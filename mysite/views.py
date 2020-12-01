#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/11/21 15:29
# @Author  : QingGe
# @FileName: views.py
# @Software: PyCharm

from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from blog.models import Blog

from read_statistics.utils import get_seven_days_date, get_today_hot_data, get_yesterday_hot_data, get_7_days_hot_blogs


def home(requset):
    """ 主页 """
    blog_content_type = ContentType.objects.get_for_model(Blog)
    read_nums, dates = get_seven_days_date(blog_content_type)  # 获取7天的阅读数量

    # 获取7天热门博客的缓存数据  此缓存需要在setting.py中进行配置
    hot_blogs_for_7_days = cache.get('hot_blogs_for_7_days')
    if hot_blogs_for_7_days is None:
        hot_blogs_for_7_days = get_7_days_hot_blogs()  # 获取7天的博客阅读数量排行
        cache.set('hot_blogs_for_7_days', hot_blogs_for_7_days, 3600)  # 键值对形式进行存储 3600秒

    content = {}
    content['read_nums'] = read_nums
    content['dates'] = dates
    content['today_hot_data'] = get_today_hot_data(blog_content_type)  # 获取当天的博客阅读数量排行
    content['yesterday_hot_data'] = get_yesterday_hot_data(blog_content_type)  # 获取昨天的博客阅读数量排行
    content['hot_blogs_for_7_days'] = hot_blogs_for_7_days  # 获取7天的博客阅读数量排行
    return render(requset, "home.html", content)
