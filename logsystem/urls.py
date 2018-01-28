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
from django.contrib import admin
from logreg.views import index, login_view, logout_view, register
from django.conf.urls import url
from board.views import test_page

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', login_view,name='login'),
    url(r'^register/$', register, name='register'),
    url(r'^index/$', index,name='index'),
    url(r'^logout/$', logout_view,name='logout'),
    url(r'^$', index, name='main'),

]