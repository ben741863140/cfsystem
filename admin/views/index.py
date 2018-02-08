from django.shortcuts import render, redirect
from board.models import CFUser
import re
from board.utility import get_rating


def index(request):
    if not request.user.is_authenticated or request.user.is_superuser == 0:
        return redirect('/')
    return render(request, 'admin/modify.html', {'users': CFUser.objects.all()})


def del_cf_users(request):
    if not request.user.is_authenticated or request.user.is_superuser == 0:
        return redirect('/')
    if request.method != 'POST':
        redirect('/')
    for handle in request.POST.getlist('users[]'):
        CFUser.objects.filter(handle=handle).get().delete()
    return render(request, 'admin/modify.html', {'users': CFUser.objects.all()})


def _deal_list(text):  # not a view function
    results = []
    visit = []
    for line in text.split('\n'):
        line = line.strip()
        if len(line) == 0:
            continue
        res = get_user_info(line)
        res['text'] = line
        if res['status'] == 'OK':
            if res['handle'] in visit:
                res['comment'] = 'handle: ' + res['handle'] + '与上面重复'
            else:
                visit.append(res['handle'])
        results.append(res)
    return {'results': results, 'handles': visit}


def _update_cf_user(res): #not a view
    if res['status'] != 'OK':
        return
    if len(CFUser.objects.filter(handle=res['handle'])) == 0:
        CFUser.objects.create(handle=res['handle'], rating=res['rating'], realname=res['realname'])
    else:
        user = CFUser.objects.filter(handle=res['handle']).get()
        user.rating = res['rating']
        if res['realname']:
            user.realname = res['realname']
        user.save()


def list_add(request):
    if not request.user.is_authenticated or request.user.is_superuser == 0:
        return redirect('/')
    if request.method == 'POST':
        msg = _deal_list(request.POST['list'])
        for res in msg['results']:
            _update_cf_user(res)
        msg['results'].sort(key=lambda x: x['status'])
        return render(request, 'admin/add_result.html', context=msg)
    return render(request, 'admin/list_add.html')


def list_override(request):
    if not request.user.is_authenticated or request.user.is_superuser == 0:
        return redirect('/')
    if request.method == 'POST':
        msgs = _deal_list(request.POST['list'])
        handles = msgs['handles']
        deleted = []
        for user in CFUser.objects.all():
            if user.handle not in handles:
                res = {'status': 'OK', 'comment': '删除成功', 'handle': user.handle, 'realname': user.realname}
                msgs['results'].append(res)
                deleted.append(user.handle)
                user.delete()
        for res in msgs['results']:
            if res['status'] == 'OK' and res['handle'] not in deleted:
                _update_cf_user(res)
        return render(request, 'admin/add_result.html', context=msgs)
    return render(request, 'admin/list_override.html')


def get_user_info(line):
    handle = re.findall(re.compile(r'[0-9a-zA-Z_]{3,24}'), line)
    realname = re.findall(re.compile(r'[\u4e00-\u9fa5]{2,3}'), line)
    if len(handle) == 0 or len(handle) > 1 or len(realname) > 1:
        return {'status': 'FAILED', 'comment': '无法识别'}
    if len(realname) == 0:
        realname.append('')
    handle = handle[0].lower()
    res = {'realname': realname[0], 'handle': handle}
    if len(CFUser.objects.filter(handle=handle)) != 0:
        res['rating'] = CFUser.objects.filter(handle=handle).get().rating
        res['status'] = 'OK'
        return res
    res.update(get_rating(handle[0]))
    return res
