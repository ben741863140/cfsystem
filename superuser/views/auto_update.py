from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from board.auto_update import UpdateSetting, AutoUpdate


def set_auto_update(request):
    if not request.user.is_authenticated or request.user.is_superuser == 0:
        return HttpResponseRedirect('..')
    if 'hour' in request.GET.keys():
        get = request.GET.copy()
        get['is_open'] = True if get['is_open'] == 'true' else False
        UpdateSetting(is_open=get['is_open'], hour=get['hour'], minute=get['minute']).write_setting()
        return JsonResponse({})
    return render(request, 'superuser/auto_update/set_auto_update.html')


def get_config(request):
    if not request.user.is_authenticated or request.user.is_superuser == 0:
        return HttpResponseRedirect('..')
    setting = UpdateSetting()
    setting.load_setting()
    info = {'is_open': setting.is_open, 'hour': setting.hour, 'minute': setting.minute}
    return JsonResponse(info)


def finished(request):
    return render(request, 'superuser/auto_update/finished.html')


def manual_update(request, only_board=False):
    if request.user.is_authenticated and request.user.is_superuser:
        AutoUpdate.update(only_board)
    return redirect('/admin')
