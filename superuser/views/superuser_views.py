from django.shortcuts import render, redirect
from board.models import CFUser
import re, datetime
from board.utility import get_rating
from superuser.forms import StaticBoardForm
from board.models import Board, BoardItem
from board.utility import get_rating_change

def Userlist(request):
    if not request.user.is_authenticated or request.user.is_superuser == 0:
        return redirect('/')
    return render(request, 'superuser/handle_controller.html', {'users': CFUser.objects.all()})

def modify(request):
    if not request.user.is_authenticated or request.user.is_superuser == 0:
        return redirect('/')
    return render(request, 'superuser/modify.html', {'boards': Board.objects.all()})


# def _get_max_rating(rating_changes, start_time, end_time, number=1):
#     ratings = []
#     for change in rating_changes:
#         time = datetime.datetime.fromtimestamp(change['ratingUpdateTimeSeconds'])
#         if start_time <= time < end_time:
#             ratings.append(change['newRating'])
#             # max_rating = max(max_rating, change['newRating'])
#
#     ratings.sort(key=lambda x: x['newRating'], reverse=True)
#     max_rating = 0
#     for i in range(number):
#         max_rating += ratings[i]
#     return max_rating


def create_board(request):
    if not request.user.is_superuser or not request.user.is_authenticated:
        redirect('/')
    form = StaticBoardForm()
    if request.method == 'POST':
        form = StaticBoardForm(request.POST)
        print(form.data)
        if form.is_valid():
            results = _deal_list(form.cleaned_data.get('list_text'))['results']
            print(results)
            clean_data = form.cleaned_data
            board = Board(name=clean_data['name'],
                          start_time=clean_data['start_time'],
                          end_time=clean_data['end_time'], type=clean_data['type'], creator=request.user)
            board.save()
            for msg in results:
                if msg['status'] != 'OK':
                    continue
                cf_user = CFUser.objects.get_or_create(handle=msg['handle'])[0]
                cf_user.realname = msg['realname']
                cf_user.rating = msg['rating']
                cf_user.save()
                board_item = BoardItem(board=board, cf_user=cf_user, max_rating=0, old_rating=0)
                # rating_changes = get_rating_change(msg['handle'])
                # board_item.max_rating = _get_max_rating(rating_changes, board.start_time, board.end_time)
                # board_item.old_rating = _get_max_rating(rating_changes, datetime.datetime.fromtimestamp(100000),
                #                                         board.start_time)
                # if board_item.old_rating == 0:
                #     board_item.old_rating = 1500
                board_item.save()
            return render(request, 'superuser/import_result.html', {'results': results})
    return render(request, 'superuser/create_board_form.html', {'form': form})


def delete_board(request):
    if request.is_ajax() and request.user.is_authenticated and request.user.is_superuser and request.method == 'POST':
        ids = request.POST.getlist('ids[]')
        for ID in ids:
            Board.objects.filter(id=ID).delete()
            print('删除id为', ID, '的榜单')
        return render(request, 'superuser/modify.html', {'boards': Board.objects.all()})
    return redirect('/')


def del_cf_users(request):
    if not request.user.is_authenticated or request.user.is_superuser == 0:
        return redirect('/')
    if request.method != 'POST':
        redirect('/')
    for handle in request.POST.getlist('users[]'):
        CFUser.objects.filter(handle=handle).get().delete()
    return render(request, 'superuser/modify.html', {'users': CFUser.objects.all()})


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


def _update_cf_user(res):  # not a view
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
        return render(request, 'superuser/add_result.html', context=msg)
    return render(request, 'superuser/list_add.html')


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
        return render(request, 'superuser/add_result.html', context=msgs)
    return render(request, 'superuser/list_override.html')


def get_user_info(line):
    handle = re.findall(re.compile(r'[0-9a-zA-Z_]{3,24}'), line)
    realname = re.findall(re.compile(r'[\u4e00-\u9fa5]{2,3}'), line)
    if len(handle) != 1 or len(realname) > 1:
        return {'status': 'FAILED', 'comment': '无法识别'}
    if len(realname) == 0:
        realname.append('')
    handle = handle[0].lower()
    realname = realname[0]
    res = {'realname': realname, 'handle': handle}
    if len(CFUser.objects.filter(handle=handle)) != 0:
        res['rating'] = CFUser.objects.filter(handle=handle).get().rating
        res['status'] = 'OK'
        return res
    res.update(get_rating(handle))
    return res
