# Generated by Django 3.1.3 on 2020-11-24 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=256)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note_id', models.CharField(max_length=256)),
                ('uri', models.URLField()),
                ('url', models.URLField()),
                ('content', models.TextField()),
                ('account_id', models.CharField(max_length=256)),
                ('account_username', models.CharField(max_length=256)),
                ('account_display_name', models.CharField(max_length=256)),
                ('read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField()),
            ],
        ),
    ]