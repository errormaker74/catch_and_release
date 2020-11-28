import os
import sys
import json
from enum import Enum

from django.conf import settings
from django.core.management.base import BaseCommand
from ...models import Interest
from asgiref.sync import sync_to_async

import asyncio
import socket
import websockets
import requests


class PayloadKey(Enum):
    EVENT = 'event'
    UPDATE = 'update'
    PAYLOAD = 'payload'
    ACCOUNT = 'account'
    BOT = 'bot'
    LANGUAGE = 'language'
    CONTENT = 'content'
    DISPLAY_NAME = 'display_name'
    URL = 'url'


async def post2slack(params: dict) -> None:
    url = 'https://slack.com/api/chat.postMessage'
    headers = {'Content-Type': 'application/json'}
    requests.post(
        url=url,
        headers=headers,
        params=params
    )


class Command(BaseCommand):
    help = 'Collect the notes of public timeline.'

    def __init__(self):
        super().__init__()
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        self.uri = settings.STREAMING_URL
        self.slack_token = settings.SLACK_TOKEN
        self.slack_channel = settings.SLACK_CHANNEL

    async def callback(self, data: str, interests: list):

        message = json.loads(data)

        if PayloadKey.EVENT.value not in message.keys():
            # event キーが存在しない場合
            return

        if message[PayloadKey.EVENT.value] != PayloadKey.UPDATE.value:
            # update 以外は無視
            return

        payload = json.loads(message[PayloadKey.PAYLOAD.value])

        # botか否か
        if PayloadKey.ACCOUNT.value in payload.keys() \
                and PayloadKey.BOT.value in payload[PayloadKey.ACCOUNT.value].keys() \
                and payload[PayloadKey.ACCOUNT.value][PayloadKey.BOT.value]:
            # bot の場合は無視
            return

        # 日本語設定のインスタンスか
        if PayloadKey.LANGUAGE.value in payload.keys() \
                and payload[PayloadKey.LANGUAGE.value] != 'ja':
            # 日本語設定のインスタンスでない場合は無視
            return

        hit = False
        c = payload[PayloadKey.CONTENT.value].lower()
        for i in set(interests):
            if i in c:
                hit = True
                break

        if hit:
            display_name = payload[PayloadKey.ACCOUNT.value][PayloadKey.DISPLAY_NAME.value]
            content = payload[PayloadKey.CONTENT.value]
            url = payload[PayloadKey.URL.value]
            params = {
                'token': self.slack_token,
                'channel': self.slack_channel,
                'text': f'name:{display_name}\nurl:{url}\ncontent:{content}',
            }
            await post2slack(params)

    async def main(self) -> None:

        sleep_time: int = 60
        reply_timeout: int = 60
        ping_timeout: int = 60

        while True:
            try:
                interests = [i.word.lower() for i in await sync_to_async(Interest.objects.all)()]
                async with websockets.connect(self.uri) as ws:
                    while True:
                        try:
                            reply = await asyncio.wait_for(ws.recv(), timeout=reply_timeout)
                        except (asyncio.TimeoutError, websockets.exceptions.ConnectionClosed):
                            try:
                                pong = await ws.ping()
                                await asyncio.wait_for(pong, timeout=ping_timeout)
                                continue
                            except:
                                await asyncio.sleep(sleep_time)
                                break
                        await self.callback(data=reply, interests=interests)

            except socket.gaierror:
                await asyncio.sleep(sleep_time)
                continue
            except ConnectionRefusedError:
                await asyncio.sleep(sleep_time)
                continue
            except websockets.exceptions.InvalidStatusCode as e:
                if e.status_code == 502:
                    sys.exit(1)
                await asyncio.sleep(sleep_time)
                continue

    def add_arguments(self, parser) -> None:
        pass

    def handle(self, *args, **options) -> None:
        asyncio.get_event_loop().run_until_complete(self.main())
