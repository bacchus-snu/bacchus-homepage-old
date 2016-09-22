# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('read_count', models.IntegerField(default=0)),
                ('comment_count', models.IntegerField(default=0)),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('modified_datetime', models.DateTimeField(auto_now_add=True)),
                ('is_secret', models.BooleanField(default=False)),
                ('content', models.TextField(default=b'')),
                ('username', models.CharField(max_length=64)),
                ('user_id', models.CharField(max_length=64, blank=True)),
                ('bs_year', models.IntegerField()),
                ('password', models.CharField(max_length=128, blank=True)),
                ('email', models.CharField(max_length=256)),
                ('homepage', models.CharField(max_length=256, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('title', models.CharField(max_length=64)),
                ('article_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('content', models.TextField()),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=64)),
                ('user_id', models.CharField(max_length=64)),
                ('bs_year', models.IntegerField()),
                ('email', models.CharField(max_length=256)),
                ('article', models.ForeignKey(to='homepage.Article')),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=16)),
                ('bs_number', models.IntegerField()),
                ('team', models.IntegerField(default=4, choices=[(0, b'Head'), (1, b'Web'), (2, b'Linux'), (3, b'Window'), (4, b'Probation'), (5, b'Dispatched'), (6, b'OB')])),
            ],
        ),
        migrations.CreateModel(
            name='MemberInfo',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('hakbun', models.IntegerField()),
                ('email', models.CharField(max_length=200)),
                ('group', models.IntegerField()),
                ('history', models.CharField(max_length=1000)),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='board',
            field=models.ForeignKey(to='homepage.Board'),
        ),
    ]
