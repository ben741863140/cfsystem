from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from board.auto_update import get_settings, set_settings


def set_auto_update(request):
    if not request.user.is_authenticated or request.user.is_superuser == 0:
        return HttpResponseRedirect('..')
    if 'hour' in request.GET.keys():
        get = request.GET.copy()
        get['is_open'] = True if get['is_open']=='true' else False
        set_settings(get)
        return JsonResponse({})
    return render(request, 'admin/auto_update/set_auto_update.html')


def get_config(request):
    if not request.user.is_authenticated or request.user.is_superuser == 0:
        return HttpResponseRedirect('..')
    info = get_settings()
    return JsonResponse(info)
