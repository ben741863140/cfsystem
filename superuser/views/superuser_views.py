# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from logreg.models import User
import re
import datetime
from board.utility import get_rating
from django.http import HttpResponse
import json
from superuser.forms import StaticBoardForm
from board.models import Board, BoardItem, CFUser
from xlwt import *
import io


def excel_export(request):
    """
        导出excel表格
        """
    if not request.user.is_authenticated or request.user.is_superuser == 0:
        return redirect('/')
    list_obj = User.objects.all().order_by("username")
    if list_obj:
        # 创建工作薄
        ws = Workbook(encoding='utf-8')
        w = ws.add_sheet(u"数据报表")
        w.write(0, 0, u"账号")
        w.write(0, 1, u"CFID")
        w.write(0, 2, u"真名")
        w.write(0, 3, u"昵称")
        # 写入数据
        excel_row = 1
        for obj in list_obj:
            data_id = obj.username
            data_user = obj.handle
            data_realname = obj.realname
            data_nickname = obj.nickname
            w.write(excel_row, 0, data_id)
            w.write(excel_row, 1, data_user)
            w.write(excel_row, 2, data_realname)
            w.write(excel_row, 3, data_nickname)
            excel_row += 1
        # 检测文件是够存在
        # 方框中代码是保存本地文件使用，如不需要请删除该代码
        ###########################
        # exist_file = os.path.exists("test.xls")
        # if exist_file:
        #     os.remove(r"test.xls")
        # ws.save("test.xls")
        ############################
        sio = io.BytesIO()
        ws.save(sio)
        sio.seek(0)
        response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=名单.xls'
        response.write(sio.getvalue())
        return response


def list_user(request):
    if not request.user.is_authenticated or request.user.is_superuser == 0:
        return redirect('/')
    return render(request, 'superuser/handle_controller.html', {'users': User.objects.all()})


def edit_handle(request):
    if not request.user.is_authenticated or request.user.is_superuser == 0:
        return redirect('/')
    # print(233)
    if request.is_ajax():
        hand = str(request.POST.get('hand'))
        realname = str(request.POST.get('realname'))
        username = str(request.POST.get('username'))
        nickname = str(request.POST.get('nickname'))
        user_id = request.POST.get('id')
        is_super = str(request.POST.get('super'))
        print(user_id)
        # print(233)
        obj = User.objects.get(id=user_id)
        print(obj.realname)
        if is_super == 'true':
            obj.is_superuser = True
        else:
            obj.is_superuser = False
        obj.realname = realname
        obj.handle = hand
        obj.username = username
        obj.nickname = nickname
        obj.save()
        return_json = {}
        return HttpResponse(json.dumps(return_json), content_type='application/json')


def delete_handle(request):
    if not request.user.is_authenticated or request.user.is_superuser == 0:
        return redirect('/')
    # print(233)
    if request.is_ajax():
        user_id = request.POST.get('id')
        print(user_id)
        # print(233)
        User.objects.filter(id=user_id).delete()
        return_json = {}
        return HttpResponse(json.dumps(return_json), content_type='application/json')


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


def get_user_info(line):
    handle = re.findall(re.compile(r'[0-9a-zA-Z_-]{3,24}'), line)
    realname = re.findall(re.compile(r'[\u4e00-\u9fa5]{2,30}'), line)
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
