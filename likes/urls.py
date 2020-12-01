#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/11/28 14:12
# @Author  : QingGe
# @FileName: urls.py
# @Software: PyCharm


from django.urls import path
from .views import like_change

urlpatterns = [
    path('like_change/', like_change, name='like_change')
]
