#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/11/24 20:41
# @Author  : QingGe
# @FileName: urls.py
# @Software: PyCharm
from django.urls import path
from .views import update_comment

urlpatterns = [
    path('update_comment/', update_comment, name='update_comment')
]
