#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/11/28 14:58
# @Author  : QingGe
# @FileName: likes_tags.py
# @Software: PyCharm


from django import template
from django.contrib.contenttypes.models import ContentType
from likes.models import LikeCount, LikeRecord

register = template.Library()


@register.simple_tag
def get_like_count(obj):
    """
        获取博客点赞数量
    :param obj: 博客对象
    :return: 点赞数量
    """
    content_type = ContentType.objects.get_for_model(obj)
    like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=obj.pk)
    return like_count.like_num


@register.simple_tag(takes_context=True)  # 加入这个可以使用所在模板的变量
def get_like_status(context, obj):
    """
        获取点赞状态
            1. 用户登录的情况
                如果点赞了此博客，加入 class=active 。使得页面点赞部分为红色
                如果没有点赞此博客，加入 class='' 。 使得页面点赞部分为默认颜色（未进行点赞）
            2. 用户未登录的情况
                只会显示页面点赞部分为默认颜色（未进行点赞）
    :param context: 模板变量
    :param obj: 博客对象
    :return: class属性值
    """
    content_type = ContentType.objects.get_for_model(obj)
    user = context['user']
    if not user.is_authenticated:
        return ''
    if LikeRecord.objects.filter(content_type=content_type, object_id=obj.pk, user=user).exists():
        return 'active'
    else:
        return ''


@register.simple_tag
def get_content_type(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return content_type.model


