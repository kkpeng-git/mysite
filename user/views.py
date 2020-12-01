#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/11/29 2:25
# @Author  : QingGe
# @FileName: 12312.py
# @Software: PyCharm
import string
import random
import time
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import JsonResponse
from django.core.mail import send_mail
from .forms import LoginForm, RegForm, ChangeNicknameForm, BindEmailForm, ChangePasswordForm, ForgetPasswordForm
from .models import Profile


def login_for_medal(requset):
    """ ajax 登陆 """
    login_form = LoginForm(requset.POST)
    data = {}
    if login_form.is_valid():  # 判断提交的数据是否合法
        user = login_form.cleaned_data['user']  # 这里的['user'] 是在form中定义的
        auth.login(requset, user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)


def login(requset):
    """ 登陆 """
    if requset.method == "POST":
        login_form = LoginForm(requset.POST)
        if login_form.is_valid():  # 判断提交的数据是否合法
            user = login_form.cleaned_data['user']  # 这里的['user'] 是在form中定义的
            auth.login(requset, user)
            return redirect(requset.GET.get('from', reverse('home')))  # 重定向到前一个页面，如果没有传from(GET方法)，就到首页
    else:  # GET 返回页面
        login_form = LoginForm()

    content = {}
    content['login_form'] = login_form
    return render(requset, 'user/login.html', content)


def register(requset):
    """ 注册 """
    if requset.method == "POST":
        reg_form = RegForm(requset.POST, requset=requset)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            # 创建用户
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            ).save()
            # 清除session
            del requset.session['register_code']
            # 登录用户  注册完之后自动登陆，跳转
            user = auth.authenticate(username=username, password=password)  # 用户验证
            auth.login(requset, user)
            return redirect(requset.GET.get('from', reverse('home')))  # 重定向到前一个页面，如果没有传from(GET方法)，就到首页
    else:  # GET 返回页面
        reg_form = RegForm()

    content = {}
    content['reg_form'] = reg_form
    return render(requset, 'user/register.html', content)


def logout(requset):
    """ 注销 退出当前用户 """
    auth.logout(requset)
    return redirect(requset.GET.get('from', reverse('home')))  # 重定向到前一个页面，如果没有传from(GET方法)，就到首页


def user_info(requset):
    """ 个人信息 """
    context = {}
    return render(requset, 'user/user_info.html', context=context)


def change_nickname(requset):
    """ 修改昵称 """
    redirect_to = requset.GET.get('from', reverse('home'))
    if requset.method == 'POST':
        form = ChangeNicknameForm(requset.POST, user=requset.user)
        if form.is_valid():
            nickname_new = form.cleaned_data['nickname_new']
            profile, created = Profile.objects.get_or_create(user=requset.user)
            profile.nickname = nickname_new
            profile.save()
            return redirect(redirect_to)
    else:
        form = ChangeNicknameForm()
    context = {}
    context['form'] = form
    context['page_title'] = '修改昵称'
    context['form_title'] = '修改昵称'
    context['submit_text'] = '修改'
    context['return_back_url'] = redirect_to
    return render(requset, 'form.html', context)


def bind_email(requset):
    """ 绑定邮箱 """
    redirect_to = requset.GET.get('from', reverse('home'))
    if requset.method == 'POST':
        form = BindEmailForm(requset.POST, requset=requset)
        if form.is_valid():
            email = form.cleaned_data['email']
            requset.user.email = email
            requset.user.save()
            # 清除session
            del requset.session['bind_email_code']
            return redirect(redirect_to)
    else:
        form = BindEmailForm()
    context = {}
    context['form'] = form
    context['page_title'] = '绑定邮箱'
    context['form_title'] = '绑定邮箱'
    context['submit_text'] = '绑定'
    context['return_back_url'] = redirect_to
    return render(requset, 'user/bind_email.html', context)


def send_verification_code(requset):
    """ 发送邮箱验证码 """
    email = requset.GET.get('email', '')
    send_for = requset.GET.get('send_for', '')
    data = {}
    if email != '':
        # 生成验证码
        code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        # 30秒之内不再发送
        now = int(time.time())
        send_code_time = requset.session.get('send_code_time', 0)
        if now - send_code_time < 30:
            data['status'] = 'ERROR'
        else:
            requset.session[send_for] = code
            requset.session['send_code_time'] = now
            # 发送邮件
            send_mail(
                '绑定邮箱',
                '验证码：%s' % code,
                '18273390852@163.com',
                [email],
                fail_silently=False,
            )
            data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)


def change_password(requset):
    """ 修改密码 """
    redirect_to = reverse('home')
    if requset.method == 'POST':
        form = ChangePasswordForm(requset.POST, user=requset.user)
        if form.is_valid():
            user = requset.user
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            auth.logout(requset)  # 登出
            return redirect(redirect_to)
    else:
        form = ChangePasswordForm()
    context = {}
    context['form'] = form
    context['page_title'] = '修改密码'
    context['form_title'] = '修改密码'
    context['submit_text'] = '修改'
    context['return_back_url'] = redirect_to
    return render(requset, 'form.html', context)


def forget_password(requset):
    """ 忘记密码 """
    redirect_to = reverse('login')
    if requset.method == 'POST':
        form = ForgetPasswordForm(requset.POST, requset=requset)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password']
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            # 清除session
            del requset.session['forget_password_code']
            return redirect(redirect_to)
    else:
        form = ForgetPasswordForm()
    context = {}
    context['form'] = form
    context['page_title'] = '重置密码'
    context['form_title'] = '重置密码'
    context['submit_text'] = '重置'
    context['return_back_url'] = redirect_to
    return render(requset, 'user/forget_password.html', context)
