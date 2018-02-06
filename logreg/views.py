# _*_ coding: utf-8 _*_
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
import random
from board.send_message import send_message

# Create your views here.
cap = ""
hint = '验证码不正确！'
white = ""

@csrf_exempt
def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    global cap
    global hint
    global white
    redirect_to = request.POST.get('next', request.GET.get('next',''))
    if request.is_ajax() == False and request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if str(request.POST.get('yzm')) == str(cap):
                print(233)
                form.save()
                if redirect_to:
                    return redirect(redirect_to)
                else:
                    return redirect('/')
            else:
                print(666)
                print(str(request.POST.get('yzm')))

                print(str(cap))
                return render(request, 'logreg/register.html',context={'form': form, 'hint': hint})
    else:
        form = RegisterForm()
    return render(request, 'logreg/register.html',context={'form':form, 'hint': white})

@csrf_exempt
def yz(request):
    global cap
    if request.is_ajax():
        return_json = {'result': '已发送验证码到您的cf账号，请<a href="http://www.codeforces.com" target="_blank">登录cf账号</a>，打开对话版块查看验证码(PS:当CF有比赛进行的时候，本系统不会发出验证码，届时请耐心等待比赛结束)'}
        hand = str(request.POST.get('hand'))
        print(hand)
        random.seed()
        cap = ""
        for temp in range(0,6):
            cap += random.choice('abcdefhjklmnopqrstuvwxyz0123456789')
        mes = str('Your handle is being linked to the SCAU_CFsystem. The verify code is '+ str(cap) + '. If the operator is not yourself, please ignore this message.')
        # print(cap)
        send_message(str(hand),mes)
        return HttpResponse(json.dumps(return_json), content_type='application/json')

@csrf_exempt
def yzm(request):
    global cap
    return HttpResponse(cap)

def index(request):
    return render(request,'index.html')


def base(request):
    return render(request, 'base.html', {'user':request.user, 'request':request})