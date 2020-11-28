
# catch_and_release

MastodonインスタンスのStreaming APIにつないで興味のある単語を含むTootを捕まえてSlackのチャンネルへ流すアプリです。

## インストール

- `pip install -r requirements.txt`

### secrets.jsonの設定

下記のコマンドでsecrets.jsonを生成して必要な値を設定します。

```
$ python config/gen_secrets.py
```

```
{
  "SECRET_KEY": "<secret key がランダムで生成される>",
  "SLACK_TOKEN": "",
  "SLACK_CHANNEL": "",
  "STREAMING_URL": ""
}
```


#### `SLACK_TOKEN`の設定

1. slackのbotを作成
2. slackのAPI TOKENを取得
3. slackでチャンネルを作成したあと、そのチャンネルでbotを招待する
    - 例：`/invite @your_bot`
4. secrets.jsonの`SLACK_TOKEN`に2.で作成したAPI TOKENを設定

#### `SLACK_CHANNEL`の設定

作成したslackのチャンネル名をsecrets.jsonの`SLACK_CHANNEL`に設定します。

#### `STREAMING_URL`の設定と調べ方

Mastodonのstreamingのurlを設定する。

1. Mastodonインスタンスからインスタンス情報を取得
    - 例：`https://example.com`というインスタンスの場合 `https://example.com/api/v1/instance`にアクセス。
2. JSON内のstreaming_apiのURLを取得
    - 例：`{"streaming_api":"wss://example.com"}`
3. ローカルタイムライン(LTL)もしくは連合タイムライン(FTL)のURLを組み立てる
    - 例：LTLの場合 `wss://example.com/api/v1/streaming/?stream=public:local`
    - 例：FTLの場合 `wss://example.com/api/v1/streaming/?stream=public`
4. secrets.jsonの`STREAMING_URL`に3.で組み立てたURLを設定する

### データベース作成

興味のある単語を登録しておくためのデータベースを作成します。

```
$ python manage.py migrate
```

### 管理ユーザの作成

管理サイトに入るためのsuperuserを作ります。

```
$ python manage.py createsuperuser
```

```
Username: 任意のユーザ
Email address: 任意のメールアドレス
Password: 任意のパスワード
Password (again): 任意のパスワード(確認のため再度入力)
Superuser created successfully.
```

## 使い方

### 興味のある単語の登録

webアプリを起動します。

```
$ python manage.py runserver --insecure
```

ブラウザから http://localhost:8000/admin/ にアクセスして上記で作成した管理ユーザでログインします。

Notesの欄にInterestsがあるのでそこから単語を登録します。

### 捕捉と転送

下記のコマンドでキーワードを含むTootの捕捉とSlackへの転送を開始します。

```
$ python manage.py catch_and_release
```

停止したい場合は`ctrl + c`で止まります。
