# _*_ coding: utf-8 _*_
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
import random
from board.send_message import send_message
from logreg.models import User
from board.models import RatingChange, CFUser
from board.update import update_rating, update_rating_change

cap = ""


@csrf_exempt
def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    global cap
    global hint
    global white
    redirect_to = request.POST.get('next', request.GET.get('next', ''))
    if request.is_ajax() == False and request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if str(request.POST.get('yzm')) == str(cap):
                form.save()
                handle = form.cleaned_data['handle']
                realname = form.cleaned_data['realname']
                user = User.objects.filter(handle=handle).get()
                CFUser.objects.update_or_create(handle=handle, defaults={
                    'realname': realname, 'user': user})
                update_rating(handle)
                update_rating_change(handle)
                if redirect_to:
                    return redirect(redirect_to)
                else:
                    return redirect('/')
            else:
                return render(request, 'logreg/register.html', context={'form': form})
    else:
        form = RegisterForm()
    return render(request, 'logreg/register.html', context={'form': form})


@csrf_exempt
def yz(request):
    global cap
    if request.is_ajax():
        return_json = {
            'result': '已发送验证码到您的cf账号，请<a href="http://www.codeforces.com" target="_blank">登录cf账号</a>，打开对话版块查看验证码(PS:当CF有比赛进行的时候，本系统不会发出验证码，届时请耐心等待比赛结束)'}
        hand = str(request.POST.get('hand'))
        # print(hand)
        random.seed()
        cap = ""
        for temp in range(0, 6):
            cap += random.choice('abcdefhjklmnopqrstuvwxyz0123456789')
        mes = str('Your handle is being linked to the SCAU_CFsystem. The verify code is ' + str(
            cap) + '. If the operator is not yourself, please ignore this message.')
        # print(cap)
        send_message(str(hand), mes)
        return HttpResponse(json.dumps(return_json), content_type='application/json')


@csrf_exempt
def yzm(request):
    global cap
    return HttpResponse(cap)


@csrf_exempt
def usercheck(request):
    tex = str(request.GET.get('tex'))
    # print(tex)
    t = 'true'
    for U in User.objects.all():
        if U.username == tex:
            t = 'false'
    if len(tex) > 150 or len(tex) == 0:
        t = 'false'
    for temp in range(0, len(tex)):
        if tex[temp] != '@' and tex[temp] != '.' and tex[temp] != '+' and tex[temp] != '-' and tex[temp] != '_' and (
                tex[temp] > '9' or tex[temp] < '0') and (tex[temp] > 'Z' or tex[temp] < 'A') and (
                tex[temp] > 'z' or tex[temp] < 'a'):
            t = 'false'
    return HttpResponse(t)


@csrf_exempt
def reset_password(request):
    redirect_to = request.POST.get('next', request.GET.get('next', ''))
    if request.method == 'POST':
        pas = str(request.POST.get('password1'))
        for user in User.objects.filter(username=request.POST.get('user')):
            user.set_password(pas)
            user.save(update_fields=["password"])
        if redirect_to:
            return redirect(redirect_to)
        else:
            return redirect('/')
    return render(request, 'registration/reset_password.html')


@csrf_exempt
def user_exist(request):
    t = 'false'
    tex = str(request.GET.get('tex'))
    if User.objects.filter(username=tex).exists():
        t = 'true'
    return HttpResponse(t)


@csrf_exempt
def yz2(request):
    global cap
    if request.is_ajax():
        return_json = {
            'result': '已发送验证码到您的cf账号，请<a href="http://www.codeforces.com" target="_blank">登录cf账号</a>，打开对话版块查看验证码(PS:当CF有比赛进行的时候，本系统不会发出验证码，届时请耐心等待比赛结束)'}
        tex = str(request.POST.get('tex'))
        # print(tex)
        for user in User.objects.filter(username=tex):
            hand = user.handle
        # print(hand)
        random.seed()
        cap = ""
        for temp in range(0, 6):
            cap += random.choice('abcdefhjklmnopqrstuvwxyz0123456789')
        mes = str('Your handle is being linked to the SCAU_CFsystem. The verify code is ' + str(
            cap) + '. If the operator is not yourself, please ignore this message.')
        # print(cap)
        send_message(str(hand), mes)
        return HttpResponse(json.dumps(return_json), content_type='application/json')


@csrf_exempt
def password_check(request):
    t = 'true'
    tex = str(request.GET.get('tex'))
    if len(tex) < 8:
        t = 'false'
    check = False
    for temp in range(0, len(tex)):
        if tex[temp] < '0' or tex[temp] > '9':
            check = True

    if check == False:
        t = 'false'
    if User.objects.filter(username=tex).exists() or User.objects.filter(handle=tex).exists():
        t = 'false'
    return HttpResponse(t)


def index(request):
    if request.user.is_authenticated:
        queryset = RatingChange.objects.filter(cf_user__handle=request.user.handle)
        data = []
        for change in queryset.filter(ratingUpdateTimeSeconds__isnull=False):
            data.append([change.ratingUpdateTimeSeconds * 1000, change.newRating])
        data = str(data)[1:-1]
        return render(request, 'index.html', {'data': data})
    else:
        return render(request, 'index.html')


def base(request):
    return render(request, 'base.html')
