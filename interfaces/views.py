# _*_ coding: utf-8 _*_

from django.http import HttpResponse
import json

from logreg.views import send_captcha_operate
from django.views.decorators.csrf import csrf_exempt

from .models import OJUser
from enum import IntEnum
from .token import create_token, check_token, get_username
from board.get_handle import get_handle
from logreg.models import Captcha
from board.views import board_list


class user_check_status(IntEnum):
    success = 0
    wrong_data = 1
    invalid_token = 2
    not_active = 3


class login_status(IntEnum):
    success = 0
    wrong_data = 1
    wrong_username = 2
    wrong_password = 3


class super_register_status(IntEnum):
    success = 0
    wrong_data = 1
    invalid_token = 2
    not_super = 3
    exist_user = 4
    wrong_handle = 5
    create_fail = 6
    exist_handle = 7


class register_status(IntEnum):
    success = 0
    wrong_data = 1
    exist_user = 2
    wrong_handle = 3
    send_fail = 4
    create_fail = 5
    exist_handle = 7


class send_captcha_status(IntEnum):
    success = 0
    wrong_data = 1
    wrong_user = 2
    wrong_handle = 3
    exist_handle = 4
    send_fail = 5


class get_board_list_status(IntEnum):
    success = 0
    wrong_data = 1
    invalid_token = 2
    not_active = 3


class get_board_status(IntEnum):
    success = 0
    wrong_data = 1
    invalid_token = 2
    not_active = 3


# 用户检查（普通用户）
def user_check(token):
    if not check_token(token):
        return user_check_status.invalid_token
    try:
        user = OJUser.objects.get(username=get_username(token))
    except OJUser.DoesNotExist:
        return user_check_status.wrong_data
    if not user.is_active:
        return user_check_status.not_active
    return user_check_status.success


# 登录
@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            if username == '' or password == '':
                return_json = {'status': login_status.wrong_data, 'token': ''}
                return HttpResponse(json.dumps(return_json), content_type='application/json')
        except ValueError:
            return_json = {'status': login_status.wrong_data, 'token': ''}
            return HttpResponse(json.dumps(return_json), content_type='application/json')
        try:
            user = OJUser.objects.get(username=username)
        except OJUser.DoesNotExist:
            return_json = {'status': login_status.wrong_username, 'token': ''}
            return HttpResponse(json.dumps(return_json), content_type='application/json')
        if user.password != password:
            return_json = {'status': login_status.wrong_password, 'token': ''}
            return HttpResponse(json.dumps(return_json), content_type='application/json')
        token = create_token(username)
        return_json = {'status': login_status.success, 'token': token}
        return HttpResponse(json.dumps(return_json), content_type='application/json')
    return_json = {'status': login_status.wrong_data, 'token': ''}
    return HttpResponse(json.dumps(return_json), content_type='application/json')


# 管理员新增用户（默认激活）
@csrf_exempt
def super_register(request):
    if request.method == 'POST':
        try:
            token = request.POST.get('token')
            username = request.POST.get('username')
            password = request.POST.get('password')
            cf_handle = request.POST.get('handle')
            is_super = request.POST.get('is_super')
            if username == '' or password == '' or cf_handle == '':
                return_json = {'status': super_register_status.wrong_data}
                return HttpResponse(json.dumps(return_json), content_type='application/json')
        except ValueError:
            return_json = {'status': super_register_status.wrong_data}
            return HttpResponse(json.dumps(return_json), content_type='application/json')
        if not check_token(token):
            return_json = {'status': super_register_status.invalid_token}
            return HttpResponse(json.dumps(return_json), content_type='application/json')
        try:
            user = OJUser.objects.get(username=get_username(token))
        except OJUser.DoesNotExist:
            return_json = {'status': super_register_status.wrong_data}
            return HttpResponse(json.dumps(return_json), content_type='application/json')
        if not user.is_super:
            return_json = {'status': super_register_status.not_super}
            return HttpResponse(json.dumps(return_json), content_type='application/json')
        temp = OJUser.objects.filter(username=username).get()
        if temp is not None and temp.is_active:
            return_json = {'status': super_register_status.exist_user}
            return HttpResponse(json.dumps(return_json), content_type='application/json')
        cf_handle = get_handle(cf_handle)
        if cf_handle == '':
            return_json = {'status': super_register_status.wrong_handle}
            return HttpResponse(json.dumps(return_json), content_type='application/json')
        temp = OJUser.objects.filter(cf_handle=cf_handle).get()
        if temp is not None and temp.is_active:
            return_json = {'status': super_register_status.exist_handle}
            return HttpResponse(json.dumps(return_json), content_type='application/json')
        try:
            if is_super != 0:
                sp = True
            else:
                sp = False
            OJUser.objects.filter(cf_handle=cf_handle).delete()
            OJUser.objects.update_or_create(username=username, cf_handle=cf_handle,
                                            defaults={'password': password, 'is_super': sp, 'is_active': True})
        except Exception:
            return_json = {'status': super_register_status.create_fail}
            return HttpResponse(json.dumps(return_json), content_type='application/json')
        return_json = {'status': super_register_status.success}
        return HttpResponse(json.dumps(return_json), content_type='application/json')
    return_json = {'status': super_register_status.wrong_data}
    return HttpResponse(json.dumps(return_json), content_type='application/json')


# 用户申请新建
@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            cf_handle = request.POST.get('cf_handle')
            if username == '' or password == '' or cf_handle == '':
                return_json = {'status': register_status.wrong_data}
                return HttpResponse(json.dumps(return_json), content_type='application/json')
        except ValueError:
            return_json = {'status': register_status.wrong_data}
            return HttpResponse(json.dumps(return_json), content_type='application/json')
        temp = OJUser.objects.filter(username=username).get()
        if temp is not None and temp.is_active:
            return_json = {'status': register_status.exist_user}
            return HttpResponse(json.dumps(return_json), content_type='application/json')
        cf_handle = get_handle(cf_handle)
        if cf_handle == '':
            return_json = {'status': register_status.wrong_handle}
            return HttpResponse(json.dumps(return_json), content_type='application/json')
        temp = OJUser.objects.filter(cf_handle=cf_handle).get()
        if temp is not None and temp.is_active:
            return_json = {'status': register_status.exist_handle}
            return HttpResponse(json.dumps(return_json), content_type='application/json')
        try:
            OJUser.objects.update_or_create(username=username, cf_handle=cf_handle,
                                            defaults={'password': password})
        except Exception:
            return_json = {'status': register_status.create_fail}
            return HttpResponse(json.dumps(return_json), content_type='application/json')
        res = send_captcha_operate(username, cf_handle)
        if res != 0:
            return_json = {'status': register_status.send_fail}
            return HttpResponse(json.dumps(return_json), content_type='application/json')
        return_json = {'status': register_status.success}
        return HttpResponse(json.dumps(return_json), content_type='application/json')
    return_json = {'status': register_status.wrong_data}
    return HttpResponse(json.dumps(return_json), content_type='application/json')


# 申请重发验证码
@csrf_exempt
def send_captcha(request):
    if request.method == 'GET':
        try:
            username = request.POST.get('username')
            cf_handle = request.POST.get('cf_handle')
            if username == '' or cf_handle == '':
                return_json = {'status': send_captcha_status.wrong_data}
                return HttpResponse(json.dumps(return_json), content_type='application/json')
        except ValueError:
            return_json = {'status': send_captcha_status.wrong_data}
            return HttpResponse(json.dumps(return_json), content_type='application/json')
        temp = OJUser.objects.filter(username=username, cf_handle=cf_handle).get()
        if temp is None or temp.is_active:
            return_json = {'status': send_captcha_status.wrong_user}
            return HttpResponse(json.dumps(return_json), content_type='application/json')
        cf_handle = get_handle(cf_handle)
        if cf_handle == '':
            return_json = {'status': send_captcha_status.wrong_handle}
            return HttpResponse(json.dumps(return_json), content_type='application/json')
        temp = OJUser.objects.filter(cf_handle=cf_handle).get()
        if temp is None or temp.is_active:
            return_json = {'status': send_captcha_status.exist_handle}
            return HttpResponse(json.dumps(return_json), content_type='application/json')
        res = send_captcha_operate(username, cf_handle)
        if res != 0:
            return_json = {'status': send_captcha_status.send_fail}
            return HttpResponse(json.dumps(return_json), content_type='application/json')
        return_json = {'status': send_captcha_status.success}
        return HttpResponse(json.dumps(return_json), content_type='application/json')
    return_json = {'status': send_captcha_status.wrong_data}
    return HttpResponse(json.dumps(return_json), content_type='application/json')


# 激活账号
def active_handle(username, cf_handle):
    try:
        oj_user = OJUser.objects.get(username=username, cf_handle=cf_handle)
    except OJUser.DoesNotExist:
        return
    oj_user.is_active = True
    oj_user.save()
    OJUser.objects.exclude(id=oj_user.id).filter(cf_handle=cf_handle).delete()
    Captcha.objects.filter(username=username).delete()
    Captcha.objects.filter(handle=cf_handle).delete()


# 查询榜单列表
@csrf_exempt
def get_board_list(request):
    data = []
    length = 0
    if request.method == 'GET':
        try:
            token = request.GET.get('token')
        except ValueError:
            return_json = {'status': get_board_list_status.wrong_data, 'data': data, 'len': length}
            return HttpResponse(json.dumps(return_json), content_type='application/json')
        temp = user_check(token)
        if temp != 0:
            return_json = {'status': temp, 'data': data, 'len': length}
            return HttpResponse(json.dumps(return_json), content_type='application/json')
        data = board_list()
        length = length(data)
        return_json = {'status': get_board_list_status.success, 'data': data, 'len': length}
        return HttpResponse(json.dumps(return_json), content_type='application/json')
    return_json = {'status': get_board_list_status.wrong_data, 'data': data, 'len': length}
    return HttpResponse(json.dumps(return_json), content_type='application/json')


# 查询榜单
@csrf_exempt
def get_board(request):
    data = []
    if request.method == 'GET':
        try:
            token = request.GET.get('token')
            board_id = request.GET.get('id')
        except ValueError:
            return_json = {'status': get_board_status.wrong_data, 'data': data}
            return HttpResponse(json.dumps(return_json), content_type='application/json')
        temp = user_check(token)
        if temp != 0:
            return_json = {'status': temp, 'data': data}
            return HttpResponse(json.dumps(return_json), content_type='application/json')
