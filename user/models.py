#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/11/29 16:52
# @Author  : QingGe
# @FileName: models.py
# @Software: PyCharm

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """ 自定义User模型 """
    # 一个表中只能有一个user  OneToOne 也就是一个用户只能有一个昵称
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="用户")
    nickname = models.CharField(max_length=20, verbose_name='昵称')

    def __str__(self):
        return '<Profile:%s for %s>' % (self.nickname, self.user.username)

    def get_nickname(self):
        """
            自定义属性
            User.get_nickname = get_nickname
        :return: nickname存在返回对应的值。不存在返回空字符串
        """
        if Profile.objects.filter(user=self).exists():
            profile = Profile.objects.get(user=self)
            return profile.nickname
        else:
            return ''

    def get_nickname_or_username(self):
        """
        """
        if Profile.objects.filter(user=self).exists():
            profile = Profile.objects.get(user=self)
            return profile.nickname
        else:
            return self.username

    def has_nickname(self):
        """ 判断是否有名称，返回布尔值 """
        return Profile.objects.filter(user=self).exists()

    User.get_nickname = get_nickname
    User.get_nickname_or_username = get_nickname_or_username
    User.has_nickname = has_nickname
