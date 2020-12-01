#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/11/24 15:11
# @Author  : QingGe
# @FileName: utils.py
# @Software: PyCharm
import datetime
from django.contrib.contenttypes.models import ContentType
from read_statistics.models import ReadNum, ReadDetaill
from django.db.models import Sum
from django.utils import timezone
from django.core.cache import caches

def read_statistics_once_read(requset, obj):
    """
    博客阅读数
        每篇博客
        每天每一个博客
    :param requset: 请求参数
    :param obj: 博客对象
    :return: cookie内容
    """
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (ct.model, obj.pk)

    if not requset.COOKIES.get(key):
        """ 统计每篇博客阅读数量  总阅读数加一 """
        # get_or_create 如果找不到就会创建 created返回的是布尔类型，如果是创建的就返回true
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        readnum.read_num += 1  # 计数加一
        readnum.save()

        """ 统计每天每一个博客阅读数量 当天阅读数加一 """
        date = timezone.now().date()  # 当天
        readDetail, created = ReadDetaill.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        readDetail.read_num += 1
        readDetail.save()
    return key


def get_seven_days_date(content_type):
    """
    获取 7 天中博客总阅读数量
    :param content_type: 对象类型 如 “博客”
    :return: 返回7天的数据 （list）
    """
    today = timezone.now().date()  # 当天
    dates = []
    read_nums = []
    for i in range(7, 0, -1):  # 7 - 0 倒着循环
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m-%d'))
        read_details = ReadDetaill.objects.filter(content_type=content_type, date=date)
        result = read_details.aggregate(read_num_sum=Sum('read_num'))  # 求和  aggregate返回一个字典  {'read_num_sum':10}
        read_nums.append(result['read_num_sum'] or 0)  # 如果result['read_num_sum']为None(false)  那么 填入 0
    return read_nums, dates


def get_today_hot_data(content_type):
    """
    获取当天阅读量 从大到小进行排序
    :param content_type: 对象类型 如 “博客”
    :return: 从大到小进行排序
    """
    today = timezone.now().date()  # 当天
    read_details = ReadDetaill.objects.filter(content_type=content_type, date=today).order_by('-read_num')  # 排序
    return read_details[:7]


def get_yesterday_hot_data(content_type):
    """
    获取昨天阅读量 从大到小进行排序
    :param content_type: 对象类型 如 “博客”
    :return: 从大到小进行排序
    """
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)  # 昨天
    read_details = ReadDetaill.objects.filter(content_type=content_type, date=yesterday).order_by('-read_num')  # 排序
    return read_details[:7]


from blog.models import Blog


def get_7_days_hot_blogs():
    """
    获取一周中博客阅读量 从大到小进行排序
    :param content_type: 对象类型 如 “博客”
    :return:  从大到小进行排序
    """
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)  # 前7天
    blogs = Blog.objects.filter(read_details__date__lt=today, read_details__date__gte=date) \
        .values('id', 'title') \
        .annotate(read_num_sum=Sum('read_details__read_num')) \
        .order_by('-read_num_sum')
    return blogs[:7]
