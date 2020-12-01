#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/11/21 14:15
# @Author  : QingGe
# @FileName: urls.py
# @Software: PyCharm

from django.urls import path
from .views import blog_detail, blog_list, blog_with_type,blog_with_date

urlpatterns = [
    # http://localhost:8000/blog/1
    path('', blog_list, name='blog_list'),
    path('<int:blog_pk>', blog_detail, name="blog_detail"),
    path('type/<int:blog_type_pk>', blog_with_type, name='blog_with_type'),
    path('date/<int:year>/<int:month>', blog_with_date, name='blog_with_date'),
]
