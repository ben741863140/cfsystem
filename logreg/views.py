# _*_ coding: utf-8 _*_
from django.shortcuts import render
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponseRedirect, HttpResponse


# Create your views here.
class UserForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=30)
    password = forms.CharField(label='密码', widget=forms.PasswordInput(), max_length=18)


class UserRigisteForm(UserForm):
    confirm_password = forms.CharField(label='确认密码', widget=forms.PasswordInput(), min_length=6,
                                                  max_length=18)


def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/index/')
    Method = request.method
    if Method == 'POST':
        # 如果有post动作，就把post的数据赋值给uf，提供给函数使用
        urf = UserRigisteForm(request.POST)
        if urf.is_valid():
            username = urf.cleaned_data['username']
            password = urf.cleaned_data['password']
            is_confirm = urf.cleaned_data['confirm_password'] = password
            queryset = User.objects.filter(username=username)

            if len(queryset) == 0:
                User.objects.create_user(username=username, password=password)
                return render(request, 'register.html', {'username': username})
            return render(request, 'register.html', {'registJudge': queryset.get()})
    else:
        urf = UserRigisteForm()
        return render(request, 'register.html', {'urf': urf, 'Method': Method})


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/index/')
    input_name =''
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            input_name = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            user = authenticate(username=input_name, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return HttpResponseRedirect('/index/')
            else:
                render(request, 'login.html', {'uf': uf})
    else:
        uf = UserForm()
    return render(request, 'login.html', {'uf': uf})


def index(request):
    uf = UserForm()
    for field in uf:
        print(type(field))
    request.session.set_expiry(0)  # 设置关闭浏览器后用session失效，就是登录的缓存
    is_logged = request.user.is_authenticated
    username = request.user.username if request.user.is_authenticated else ''
    return render(request, 'index.html', {'username': username, 'is_logged': is_logged})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/index')
