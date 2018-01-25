# _*_ coding: utf-8 _*_
from django.shortcuts import render
from django import forms
from logreg.models import User
from django.http.response import HttpResponseRedirect, HttpResponse
from django.http import response, request

# Create your views here.
class UserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=30)
    password = forms.CharField(label='密码',widget=forms.PasswordInput())

def regist(req):
    Method = req.method
    if Method=='POST':
        # 如果有post动作，就把post的数据赋值给uf，提供给函数使用
        uf = UserForm(req.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']

            try:
                registJudge = User.objects.filter(username=username).get()
                return render(req,'regist.html',{'registJudge':registJudge})
            except:
                registAdd = User.objects.create(username=username, password=password)
            # registAdd = User.objects.get_or_create(username=username,password=password)[1]
            # if registAdd == False:
                return render(req,'regist.html',{'registAdd':registAdd,'username':username})
    else:
        uf = UserForm()
        return render(req,'regist.html',{'uf':uf,'Method':Method})

def login(req):
    if req.method == 'POST':
        uf = UserForm(req.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            userPassJudge = User.objects.filter(username__exact=username,password__exact=password)

            if userPassJudge:
                response = HttpResponseRedirect('/index/')
                response.set_cookie('cookie_username',username,3600)
                return response
            else:
                return HttpResponse('login.html')
    else:
        uf = UserForm()
    return render(req,'login.html',{'uf':uf})

def index(req):
    username = req.COOKIES.get('cookie_username','')
    return render(req,'index.html',{'username':username})

def logout(req):
    # 没弄懂这个
    response = HttpResponse('logout!<br><a href="127.0.0.1:8000/regist>regist</a>"')
    response.delete_cookie('cookie_username')
    return response
