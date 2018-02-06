from django.shortcuts import render
from board.models import CFUser, RatingChange
from board.utility import get_user_info
from board.auto_update import auto_update
import datetime


def board_view(request):
    class Info:
        rank = rating = oldRating = newRating = change = handle = 0
        name = ''

    select = 'ch1'
    if 'select' in request.GET.keys():
        select = request.GET['select']
    infos = []
    time = ''
    if select == 'ch1':
        for user in CFUser.objects.all():
            info = Info()
            info.rating = user.rating
            info.handle = user.handle
            infos.append(info)
        infos.sort(key=lambda x: x.rating, reverse=True)
    else:

        days_ago = int(select[2:])
        word = {'14': '两周', '30': '一月', '90': '三月', '180': '半年'}
        time = '近' + word[str(days_ago)]
        for user in RatingChange.objects.filter(days_ago=days_ago):
            info = Info()
            info.handle = user.cf_user.handle
            info.oldRating = user.oldRating
            info.newRating = user.newRating
            info.change = user.newRating - user.oldRating
            infos.append(info)
        infos.sort(key=lambda x: x.change, reverse=True)
    for info, rank in zip(infos, range(1, len(infos) + 1)):
        info.rank = rank
        if info.change > 0:
            info.change = '+' + str(info.change)
        else:
            info.change = str(info.change)
    return render(request, 'board/board.html',
                  {'is_ch1': select == 'ch1', 'user': infos, 'Time': time, 'date': datetime.datetime.now().year})


def board_rating(request):
    class User:
        rank = rating = handle = 0

    users = []
    for user in CFUser.objects.all():
        info = User()
        info.rating = user.rating
        info.handle = user.handle
        users.append(info)
    users.sort(key=lambda x: x.rating, reverse=True)
    for i in range(len(users)): users[i].rank = i + 1
    return render(request, 'board/board_rating.html', {'users': users})


def board_upgrade(request, days_ago):
    class User:
        rank = rating = handle = oldRating = newRating = change = 0

    users = []
    word = {'14': '两周', '30': '一月', '90': '三月', '180': '半年'}
    time = '近' + word[str(days_ago)]
    for user in RatingChange.objects.filter(days_ago=days_ago):
        info = User()
        info.change = user.newRating - user.oldRating
        if info.change <= 0:
            continue
        info.handle = user.cf_user.handle
        info.oldRating = user.oldRating
        info.newRating = user.newRating
        users.append(info)
    users.sort(key=lambda x: x.change, reverse=True)
    for i in range(len(users)):
        users[i].rank = i + 1
        users[i].change = '+' + str(users[i].change)
    return render(request, 'board/board_upgrade.html', {'users': users, 'time': time})


def handle_list(request):
    if 'handle_list' in request.GET.keys():
        content = request.GET['handle_list']
        results = []
        errors = []
        visit = []
        for line in content.split('\n'):
            line = line.strip()
            res = get_user_info(line)
            if res['status'] == 'OK':
                if res['handle'] in visit:
                    res['comment'] = 'handle: ' + res['handle'] + '与上面重复'
                    errors.append(res)
                else:
                    results.append(res)
                visit.append(res['handle'])
            else:
                res['text'] = line
                errors.append(res)
        for res in results:
            if len(CFUser.objects.filter(handle=res['handle'])) == 0:
                CFUser.objects.create(handle=res['handle'], rating=res['rating'], realname=res['realname'])
            else:
                user = CFUser.objects.filter(handle=res['handle']).get()
                user.rating = res['rating']
                user.realname = res['realname']
                user.save()
        return render(request, 'board/handle_result.html', {'results': results, 'errors': errors})

    return render(request, 'board/handlelist.html', {'date': datetime.datetime.now().year})


auto_update()
