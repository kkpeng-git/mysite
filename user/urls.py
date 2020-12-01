"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from .views import login, register, login_for_medal, logout, user_info, change_nickname, bind_email, \
    send_verification_code, change_password,forget_password

urlpatterns = [
    path('login_for_medal/', login_for_medal, name='login_for_medal'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('user_info/', user_info, name='user_info'),
    path('change_nickname/', change_nickname, name='change_nickname'),
    path('bind_email/', bind_email, name='bind_email'),
    path('send_verification_code/', send_verification_code, name='send_verification_code'),
    path('change_password/', change_password, name='change_password'),
    path('forget_password/', forget_password, name='forget_password'),
]
