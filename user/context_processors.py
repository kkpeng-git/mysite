#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/11/29 2:42
# @Author  : QingGe
# @FileName: fwe.py
# @Software: PyCharm

from .forms import LoginForm


def login_model_form(request):
    """
        自定义模板变量  login form表单
    """
    return {'login_model_form': LoginForm()}
