# _*_ coding: utf-8 _*_

from django.http import HttpResponse
import json
from interfaces.models import OJUser
from enum import IntEnum
from interfaces.token import create_token, check_token, get_username
from board.get_handle import get_handle


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


class register_status(IntEnum):
    success = 0
    wrong_data = 1
    exist_user = 2



# 登录
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
        if temp is not None:
            return_json = {'status': super_register_status.exist_user}
            return HttpResponse(json.dumps(return_json), content_type='application/json')
        cf_handle = get_handle(cf_handle)
        if cf_handle == '':
            return_json = {'status': super_register_status.wrong_handle}
            return HttpResponse(json.dumps(return_json), content_type='application/json')
        try:
            if is_super != 0:
                sp = True
            oj_user = OJUser.objects.create(username=username, password=password, is_super=sp, is_active=True,
                                           cf_handle=cf_handle)
            oj_user.save()
        except Exception:
            return_json = {'status': super_register_status.create_fail}
            return HttpResponse(json.dumps(return_json), content_type='application/json')
        return_json = {'status': super_register_status.success}
        return HttpResponse(json.dumps(return_json), content_type='application/json')
    return_json = {'status': super_register_status.wrong_data}
    return HttpResponse(json.dumps(return_json), content_type='application/json')


# 用户申请新建
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

    return_json = {'status': register_status.wrong_data}
    return HttpResponse(json.dumps(return_json), content_type='application/json')