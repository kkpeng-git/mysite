#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/11/27 20:17
# @Author  : QingGe
# @FileName: comment_tags.py
# @Software: PyCharm

from django import template
from django.contrib.contenttypes.models import ContentType
from comment.models import Comment
from comment.forms import CommentForm

register = template.Library()


@register.simple_tag
def get_comment_count(obj):
    """
        获取博客评论计数
    :param obj:  博客对象
    :return: 评论计数
    """
    content_type = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(content_type=content_type, object_id=obj.pk).count()


@register.simple_tag
def get_comment_form(obj):
    """
        获取博客的form表单
    :param obj: 博客对象
    :return: form表单
    """
    content_type = ContentType.objects.get_for_model(obj)
    form = CommentForm(
        initial={'content_type': content_type.model, 'object_id': obj.pk, 'reply_comment_id': '0'})
    return form


@register.simple_tag
def get_comment_list(obj):
    """
        获取博客中的评论  一级评论
    :param obj: 博客对象
    :return: 一级评论  时间排序
    """
    content_type = ContentType.objects.get_for_model(obj)
    comments = Comment.objects.filter(content_type=content_type, object_id=obj.pk, parent=None)  # parent=None为一级评论
    return comments.order_by('-comment_time')
