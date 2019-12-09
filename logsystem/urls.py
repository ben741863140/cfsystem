"""logsystem URL Configuration

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
from django.conf.urls import url, include
from django.urls import path
from logreg.views import index, send_captcha, user_check, user_exist, password_check, reset_password_captcha, receive_captcha
urlpatterns = [
    url(r'^board/', include('board.urls')),
    url(r'^logreg/', include('logreg.urls')),
    url(r'^logreg/', include('django.contrib.auth.urls')),
    url(r'^$', index, name='index'),
    url(r'^admin/', include('superuser.urls')),
    url(r'^ajax/send_captcha/', send_captcha, name='send_captcha'),
    url(r'^ajax/user_check', user_check, name='user_check'),
    url(r'^ajax/user_exist', user_exist, name='user_exist'),
    url(r'^ajax/password_check', password_check, name='password_check'),
    url(r'^ajax/reset_password_captcha/', reset_password_captcha),
    path('verify/<str:captcha>', receive_captcha),
]
