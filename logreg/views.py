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

    def clean_username(self):
        username = self.cleaned_data['username']
        queryset = User.objects.filter(username=username)
        if len(queryset) == 0:
            raise forms.ValidationError("用户不存在")
        return username

    def clean_password(self):
        username = self.data['username']
        password = self.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError("密码错误")
        return password


class UserRegisterForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=30)
    password = forms.CharField(label='密码', widget=forms.PasswordInput(), max_length=18)
    confirm_password = forms.CharField(label='确认密码', widget=forms.PasswordInput(), min_length=6,
                                       max_length=18)

    def clean_username(self):
        username = self.data['username']
        queryset = User.objects.filter(username=username)
        if len(queryset):
            raise forms.ValidationError('该用户已存在')
        return username

    def clean_confirm_password(self):
        password = self.data['password']
        confirm_password = self.data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('两次密码输入不一致')
        return confirm_password


def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/index/')
    urf = UserRegisterForm()
    return render(request, 'register.html', {'urf': urf})


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/index/')
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            input_name = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            user = authenticate(username=input_name, password=password)
            login(request, user)
            return HttpResponseRedirect('/index/')
    else:
        uf = UserForm()
    return render(request, 'login.html', {'uf': uf})


def index(request):
    uf = UserForm()
    request.session.set_expiry(0)  # 设置关闭浏览器后用session失效，就是登录的缓存
    is_logged = request.user.is_authenticated
    username = request.user.username if request.user.is_authenticated else ''
    return render(request, 'index.html', {'username': username, 'is_logged': is_logged})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/index')
