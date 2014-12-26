# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password

from homepage.const import *

class Member(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=16)
    bs_number = models.IntegerField()
    team = models.IntegerField(default=MEMBER_PROBATION, choices=MEMBER_TYPE)
    def __unicode__(self):
        team_name = u''
        for (k, v) in MEMBER_TYPE:
            if self.team == k:
                team_name = v

        return u'[%s] %s %s(%s)' % (unicode(self.id), unicode(self.bs_number), unicode(self.name), team_name)


class Board(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    article_count = models.IntegerField(default=0)
    def __unicode__(self):
        return u'[%s] (name=%s), (title=%s), (article_count=%s)' % (unicode(self.id), unicode(self.name), unicode(self.title), unicode(self.article_count))

class Article(models.Model):
    board = models.ForeignKey(Board)
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=256)
    read_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now_add=True)
    is_secret = models.BooleanField(default=False)
    content = models.TextField(default='')
    # User Info
    username = models.CharField(max_length=64)
    user_id = models.CharField(max_length=64, blank=True)
    bs_year = models.IntegerField()
    password = models.CharField(max_length=128, blank=True)
    email = models.CharField(max_length=256)
    homepage = models.CharField(max_length=256, blank=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)


class Comment(models.Model):
    article = models.ForeignKey(Article)
    id = models.AutoField(primary_key=True)
    content = models.TextField()

    created_datetime = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, null=True)

    # User Info
    name = models.CharField(max_length=64, null=True)
    email = models.CharField(max_length=128, null=True)
    password = models.CharField(max_length=128, null=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

