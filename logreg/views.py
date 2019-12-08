# _*_ coding: utf-8 _*_
import datetime
import time
import _md5
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
import random
from board.send_message import send_message
from logreg.models import User, Captcha
from board.models import RatingChange, CFUser
from board.update import update_rating, update_rating_change

ip = 'http://www.scaucf.top'


def modify_self(request):
    if not request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        nickname = str(request.POST.get('nickname'))
        obj = User.objects.get(id=request.user.id)
        obj.nickname = nickname
        obj.save()
        return redirect('/')
    return render(request, 'logreg/modify_self.html', )


@csrf_exempt
def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    redirect_to = request.POST.get('next', request.GET.get('next', ''))
    if not request.is_ajax() and request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            captcha = ""
            try:
                captcha = Captcha.objects.get(request.POST.get('handle'))
            except Exception:
                return render(request, 'logreg/register.html', context={'form': form})
            if captcha.username == str(form.cleaned_data['username']) and captcha.status == 1:
                print('captcha pass')
                temp = captcha.username
                Captcha.objects.filter(username=temp).delete()
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


def send_captcha(request):
    if request.is_ajax():
        handle = str(request.POST.get('hand'))
        user_name = str(request.POST.get('user_name'))
        if handle == '' or user_name == '':
            return_json = {
                'result': '账号为空，请重新确认'}
            return HttpResponse(json.dumps(return_json), content_type='application/json')
        try:
            User.objects.get(handle=handle)
            return_json = {
                'result': '账号已存在，请重新验证'}
            return HttpResponse(json.dumps(return_json), content_type='application/json')
        except Exception:
            # print(handle)
            random.seed()
            captcha = ""
            for temp in range(0, 6):
                captcha += random.choice('abcdefhjklmnopqrstuvwxyz0123456789')
            captcha += handle
            captcha += str(int(time.time()))
            mes = str('Your handle is being linked to the SCAU_CFsystem. The user name is ' + user_name +
                    '. If you want to verify, please click the link: ' + ip + '/verify/' + str(captcha) +
                    ' .If the operator is not yourself, please ignore this message.')
            print(mes)
            res = send_message(str(handle), mes)
            if res == -1:
                return_json = {
                    'result': '系统错误，发送验证码失败'}
            elif res == 1:
                return_json = {
                    'result': '发送验证码失败，请检查账号名或者查看cf是否在举办比赛'}
            else:
                try:
                    item = Captcha.objects.get(handle=handle, username=user_name)
                    item.captcha = captcha
                    item.update_time = datetime.datetime.now()
                except Exception:
                    item = Captcha.objects.create(handle=handle, username=user_name, update_time=datetime.datetime.now(), captcha=captcha)
                item.save()
                return_json = {
                    'result': '已发送验证链接到您的cf账号，请<a href="http://www.codeforces.com" target="_blank">登录cf账号</a>，'
                              '打开对话版块查看验证信息(PS:当CF有比赛进行的时候，本系统不会发出验证码，届时请耐心等待比赛结束)'}
            return HttpResponse(json.dumps(return_json), content_type='application/json')


def receive_captcha(request, captcha='a'):
    if request.method == 'GET':
        try:
            item = Captcha.objects.get(captcha=captcha)
            # 验证码还在有效期内
            permitted = datetime.datetime.now() - datetime.timedelta(minutes=30)
            if item.update_time.__le__(permitted):
                item.status = 1
                item.save()
        except Exception:
            return redirect('/')
        return render(request, 'logreg/verify_success.html', context={'user': item.username})


def user_check(request):
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
        t = t + User.objects.filter(username=tex).get().handle
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
        print(hand)
        random.seed()
        captcha = ""
        for temp in range(0, 6):
            captcha += random.choice('abcdefhjklmnopqrstuvwxyz0123456789')
        mes = str('Your handle is being linked to the SCAU_CFsystem. The verify code is ' + str(
            captcha) + '. If the operator is not yourself, please ignore this message.')
        print(mes)
        send_message(str(hand), mes)
        cap[str(hand)] = str(captcha)
        return HttpResponse(json.dumps(return_json), content_type='application/json')


@csrf_exempt
def yzm2(request):
    global cap
    tex = str(request.GET.get('hand'))
    hand = tex
    for user in User.objects.filter(username=tex):
        hand = user.handle
    try:
        captcha = str(cap[str(hand)])
    except KeyError:
        captcha = ""
    print(captcha)
    print(request.GET.get('hand'))
    return HttpResponse(captcha)


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

    if not check:
        t = 'false'
    if User.objects.filter(username=tex).exists() or User.objects.filter(handle=tex).exists():
        t = 'false'
    return HttpResponse(t)


def index(request):
    if request.user.is_authenticated:
        queryset = RatingChange.objects.filter(cf_user__handle=request.user.handle)
        data = []
        for change in queryset:
            data.append([change.ratingUpdateTimeSeconds * 1000, change.newRating])
        data = str(data)[1:-1]
        return render(request, 'index.html', {'data': data})
    else:
        return render(request, 'index.html')
