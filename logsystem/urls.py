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
from board.views import board_view, handle_list
from logreg.views import index, yz, yzm, usercheck, user_exist, password_check, yz2

urlpatterns = [
    # url(r'^admin/', include('admin.urls')),
    url(r'^board/$', board_view, name='board'),
    url(r'^board/handlelist$', handle_list, name='board'),
    url(r'^logreg/', include('logreg.urls')),
    url(r'^logreg/', include('django.contrib.auth.urls')),
    url(r'^$', index, name='index'),
    url(r'^admin/', include('admin.urls')),
    url(r'^ajax/yz/', yz, name='yz'),
    url(r'^ajax/yzm/', yzm, name='yzm'),
    url(r'^ajax/usercheck', usercheck, name='usercheck'),
    url(r'^ajax/user_exist', user_exist, name='user_exist'),
    url(r'^ajax/password_check', password_check, name='password_check'),
    url(r'^ajax/yz2/', yz2, name='yz2'),
]