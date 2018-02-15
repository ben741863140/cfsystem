from django.shortcuts import render
from board.models import CFUser, RatingChange
from board.auto_update import auto_update


def board_rating(request):
    class User:
        rank = rating = handle = 0
        realname = ''

    users = []
    for user in CFUser.objects.all():
        info = User()
        info.rating = user.rating
        info.handle = user.handle
        info.realname = user.realname
        users.append(info)
    users.sort(key=lambda x: x.rating, reverse=True)
    for i in range(len(users)): users[i].rank = i + 1
    return render(request, 'board/board_rating.html', {'users': users})


def board_upgrade(request, days_ago):
    class User:
        rank = rating = handle = oldRating = newRating = change = 0
        realname = ''

    users = []
    word = {'14': '两周', '30': '一月', '90': '三月', '180': '半年'}
    time = '近' + word[str(days_ago)]
    for rc in RatingChange.objects.filter(days_ago=days_ago):
        user = User()
        user.change = rc.newRating - rc.oldRating
        if user.change <= 0:
            continue
        user.handle = rc.cf_user.handle
        user.oldRating = rc.oldRating
        user.newRating = rc.newRating
        user.realname = rc.cf_user.realname
        users.append(user)
    users.sort(key=lambda x: x.change, reverse=True)
    for i in range(len(users)):
        users[i].rank = i + 1
        users[i].change = '+' + str(users[i].change)
    return render(request, 'board/board_upgrade.html', {'users': users, 'time': time})


def board_rating_change(request, handle):
    queryset = RatingChange.objects.filter(cf_user__handle=handle)
    data = []
    for change in queryset.filter(ratingUpdateTimeSeconds__isnull=False):
        data.append([change.ratingUpdateTimeSeconds * 1000, change.newRating])
    # print(str(data)[1:-1])
    data = str(data)[1:-1]
    return render(request, 'board/rating_change.html', {'data': data})


auto_update()
