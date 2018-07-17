from django.shortcuts import render, redirect
from board.models import CFUser, RatingChange, Board, BoardItem
from board.auto_update import auto_update
from board.models import Board, BoardItem


def board_rating(request, board_id=-1):
    if not request.user.is_authenticated:
        return render(request, 'index.html')

    class User:
        rank = rating = handle = oldRating = newRating = change = 0
        nickname=realname = ''

    class User2:
        rank = rating = handle = 0
        nickname=realname = ''

    users = []
    if board_id == -1:
        board_id = Board.objects.order_by('id').first().id
    time = Board.objects.filter(id=board_id).get().name
    creator = str(Board.objects.filter(id=board_id).get().creator)
    if str("rating") == str(Board.objects.filter(id=board_id).get().type) or str(Board.objects.filter(id=board_id).get().type) == 'max_three':
        for item in BoardItem.objects.filter(board=Board.objects.filter(id=board_id).get()):
            info = User2()
            info.rating = item.max_rating
            info.handle = item.cf_user.handle
            info.realname = item.cf_user.realname
            if item.cf_user.user and item.cf_user.user.nickname:
                info.nickname = '(' + item.cf_user.user.nickname + ')'
            info.times = item.times
            users.append(info)
        users.sort(key=lambda x: x.rating, reverse=True)
        for i in range(len(users)):
            users[i].rank = i + 1
        return render(request, 'board/board_rating.html',
                      {'users': users, 'time': time, 'boards': Board.objects.all(), 'creator':creator})
    else:
        for item in BoardItem.objects.filter(board=Board.objects.filter(id=board_id).get()):
            user = User()
            user.change = item.max_rating - item.old_rating
            if user.change <= 0:
                continue
            user.handle = item.cf_user.handle
            user.oldRating = item.old_rating
            user.newRating = item.max_rating
            user.realname = item.cf_user.realname
            user.times = item.times
            if item.cf_user.user:
                user.nickname = '(' + item.cf_user.user.nickname + ')'
            users.append(user)
        users.sort(key=lambda x: x.change, reverse=True)
        for i in range(len(users)):
            users[i].rank = i + 1
            users[i].change = '+' + str(users[i].change)
        return render(request, 'board/board_upgrade.html',
                      {'users': users, 'time': time, 'boards': Board.objects.all(), 'creator':creator})


def board_rating_change(request, handle):
    if request.user.is_authenticated:
        queryset = RatingChange.objects.filter(cf_user__handle=handle)
        data = []
        for change in queryset.filter(ratingUpdateTimeSeconds__isnull=False):
            data.append([change.ratingUpdateTimeSeconds * 1000, change.newRating])
        # print(str(data)[1:-1])
        data = str(data)[1:-1]
        return render(request, 'board/rating_change.html', {'data': data})
    else:
        return render(request, 'index.html')


auto_update()
