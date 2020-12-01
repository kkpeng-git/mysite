#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/11/24 21:50
# @Author  : QingGe
# @FileName: forms.py
# @Software: PyCharm
from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    """ 登陆 """
    username_or_email = forms.CharField(
        label="用户名",
        required=True,  # 如果需要填写  就写True
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "请输入用户名或邮箱"}),
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "请输入密码"}),  # 密文 小点点
        required=True,  # 如果需要填写  就写True
    )

    def clean(self):  # 在后端调用is_valid中就会执行这个方法    clean这个函数名是固定的
        """ 在form里面就进行登录时候成功的验证。  这样就不用去view里面进行使用了 """
        username_or_email = self.cleaned_data['username_or_email']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username_or_email, password=password)  # 用户验证
        if user is None:
            if User.objects.filter(email=username_or_email).exists():
                username = User.objects.get(email=username_or_email).username
                user = auth.authenticate(username=username, password=password)  # 用户验证
                if not user is None:
                    self.cleaned_data['user'] = user
                    return self.cleaned_data
                else:
                    raise forms.ValidationError('用户名或密码不正确')
            raise forms.ValidationError('用户名或密码不正确')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data


class RegForm(forms.Form):
    """ 注册 """
    username = forms.CharField(
        label="用户名",
        max_length=30,
        min_length=3,
        required=True,  # 如果需要填写  就写True
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "请输入3-30位用户名"}),
    )
    email = forms.EmailField(
        label="邮箱",
        required=True,  # 如果需要填写  就写True
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "请输入邮箱"}),
    )
    verification_code = forms.CharField(
        label="验证码",
        required=False,  # 如果需要填写  就写True
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "点击“发送验证码”发送到邮箱"})
    )
    password = forms.CharField(
        label="密码",
        min_length=6,
        required=True,  # 如果需要填写  就写True
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "请输入密码"}),  # 密文 小点点
    )
    password_again = forms.CharField(
        label="再次输入密码",
        min_length=6,
        required=True,  # 如果需要填写  就写True
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "请再次输入密码"}),  # 密文 小点点
    )

    def __init__(self, *args, **kwargs):
        if 'requset' in kwargs:
            self.requset = kwargs.pop('requset')
        super(RegForm, self).__init__(*args, **kwargs)

    def clean(self):

        return self.cleaned_data

    def clean_username(self):  # clean_username写法固定  专门针对这个username字段名进行验证
        """ 验证用户名 """
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():  # 用户名已经存在
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        """ 验证邮箱 """
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():  # 用户名已经存在
            raise forms.ValidationError('邮箱已存在')
        return email

    def clean_password_again(self):
        """ 验证两次密码 """
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError("两次输入的密码不一致")
        return password_again

    def clean_verification_code(self):
        """ 验证码不能为空 """
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
        """ 判断验证码是否正确 """
        code = self.requset.session.get('register_code', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')
        return verification_code


class ChangeNicknameForm(forms.Form):
    """ 修改昵称 """
    nickname_new = forms.CharField(
        label="新的昵称",
        max_length=20,
        required=True,  # 如果需要填写  就写True
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "请输入新的昵称"})
    )

    def __init__(self, *args, **kwargs):
        """
            此处需要在views里面传入user参数
                如：form = ChangeNicknameForm(requset.POST, user=requset.user)
        """
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangeNicknameForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登录')
        return self.cleaned_data

    def clean_nickname_new(self):
        """ 验证用户输入的昵称是否为空 """
        # 如果用户没有填写使用cleaned_data['nickname_new']是获取不到的，所以我们使用了.get方法，如果没有填写，默认为''
        nickname_new = self.cleaned_data.get('nickname_new', '').strip()
        if nickname_new == '':
            raise forms.ValidationError("新的昵称不能为空")
        return nickname_new


class BindEmailForm(forms.Form):
    """ 绑定邮箱 """
    email = forms.EmailField(
        label="邮箱",
        required=True,  # 如果需要填写  就写True
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "请输入正确的邮箱"})
    )
    verification_code = forms.CharField(
        label="验证码",
        required=False,  # 如果需要填写  就写True
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "点击“发送验证码”发送到邮箱"})
    )

    def __init__(self, *args, **kwargs):
        """
            此处需要在views里面传入user参数
                如：form = ChangeNicknameForm(requset.POST, user=requset.user)
        """
        if 'requset' in kwargs:
            self.requset = kwargs.pop('requset')
        super(BindEmailForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录
        if self.requset.user.is_authenticated:
            self.cleaned_data['user'] = self.requset.user
        else:
            raise forms.ValidationError('用户尚未登录')
        # 判断用户是否已绑定邮箱
        if self.requset.user.email != '':
            raise forms.ValidationError('你已经绑定邮箱')
        # 判断验证码
        code = self.requset.session.get('bind_email_code', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')

        return self.cleaned_data

    def clean_email(self):
        """ 验证邮箱是否存在 """
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已经绑定')
        return email

    def clean_verification_code(self):
        """ 验证码不能为空 """
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
        return verification_code


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label="旧密码",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "请输入旧密码"}),  # 密文 小点点
        required=True,  # 如果需要填写  就写True
    )
    new_password = forms.CharField(
        label="新密码",
        min_length=6,
        max_length=12,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "请输入新密码"}),  # 密文 小点点
        required=True,  # 如果需要填写  就写True
    )
    new_password_agin = forms.CharField(
        label="再次输入新密码",
        min_length=6,
        max_length=12,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "请再次输入新密码"}),  # 密文 小点点
        required=True,  # 如果需要填写  就写True
    )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        """ 验证两次密码是否输入一致 """
        new_password = self.cleaned_data.get("new_password", '')
        new_password_agin = self.cleaned_data.get("new_password_agin", '')
        if new_password_agin != new_password or new_password == '':
            raise forms.ValidationError('两次输入的密码不一致')
        return self.cleaned_data

    def clean_old_password(self):
        """ 验证旧密码是否输入正确 """
        old_password = self.cleaned_data.get('old_password', '')
        if not self.user.check_password(old_password):  # 验证密码
            raise forms.ValidationError('旧的密码错误')
        return old_password


class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(
        label="邮箱",
        required=True,  # 如果需要填写  就写True
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "请输入绑定过的邮箱"}),
    )
    verification_code = forms.CharField(
        label="验证码",
        required=False,  # 如果需要填写  就写True
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "点击“发送验证码”发送到邮箱"})
    )
    new_password = forms.CharField(
        label="新密码",
        min_length=6,
        max_length=12,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "请输入新密码"}),  # 密文 小点点
        required=True,  # 如果需要填写  就写True
    )

    def __init__(self, *args, **kwargs):
        if 'requset' in kwargs:
            self.requset = kwargs.pop('requset')
        super(ForgetPasswordForm, self).__init__(*args, **kwargs)

    def clean(self):

        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱不存在')
        return email

    def clean_verification_code(self):
        """ 验证码不能为空 """
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
        """ 判断验证码是否正确 """
        code = self.requset.session.get('forget_password_code', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')
        return verification_code
