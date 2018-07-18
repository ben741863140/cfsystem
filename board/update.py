from board import utility
from board.models import CFUser, RatingChange, User
from .models import Board
import datetime


def update_rating(handle=''):
    def update(cf_user):
        res = utility.get_rating(cf_user.handle)
        if res['status'] != 'OK':
            print('<update-rating> handle', cf_user.handle, '不存在')
            return
        cf_user.rating = res['rating']
        cf_user.save()

    if handle:
        update(CFUser.objects.filter(handle=handle).get())
    else:
        i = 0
        size = CFUser.objects.count()
        for user in CFUser.objects.all():
            update(user)
            i += 1
            # print('update rating [%d/%d]' % (i, size))


# def get_result_for_days(raw, *days_ago):
#     res = {}
#     now_rating = 0
#     for info in raw:
#         now_rating = info['newRating']
#         update_time = datetime.datetime.fromtimestamp(info['ratingUpdateTimeSeconds'])
#         # 得到的results['result']是按时间轴从以前到现在，所以遇到第一个满足条件的就是oldRating，只写进一次
#         for day in filter(lambda x: x if x not in res.keys() else None, days_ago):
#             if (datetime.datetime.now() - update_time).days <= day:
#                 res[day] = info['oldRating']
#     res['newRating'] = now_rating
#     for day in filter(lambda x: x if x not in res.keys() else None, days_ago):
#         res[day] = now_rating
#     return res


def update_rating_change(handle=''):
    def update(cf_user):
        result = utility.get_rating_change(cf_user.handle)
        queryset = RatingChange.objects.filter(cf_user__id=cf_user.id)
        for change in result:
            queryset.get_or_create(ratingUpdateTimeSeconds=change['ratingUpdateTimeSeconds'],
                                   defaults={
                                       'oldRating': change['oldRating'],
                                       'newRating': change['newRating'],
                                       'cf_user_id': cf_user.id
                                   })

    if handle:
        update(CFUser.objects.filter(handle=handle).get())
    else:
        i = 0
        # size = CFUser.objects.count()
        for user in CFUser.objects.all():
            update(user)
            i += 1
            # print('update rating change [%d/%d]' % (i, size))


def _get_max_rating(handle, start_time, end_time, number=1):
    # 使用RatingChange得到期间内最高rating, number指定使用最高的多少个RatingChange
    ratings = []
    for rc in RatingChange.objects.filter(cf_user__handle=handle).all():
        time = datetime.datetime.fromtimestamp(rc.ratingUpdateTimeSeconds)
        if start_time <= time < end_time:
            ratings.append(rc.newRating)
    ratings.sort(reverse=True)
    max_rating = 0
    for i in range(min(number, len(ratings))):
        max_rating += ratings[i]
    return int(max_rating), len(ratings)


def update_board(board_id=-1):  # -1表示更新所有Board
    if board_id == -1:
        for board in Board.objects.all():
            update_board(board.id)
        return
    # print('更新ID为%d的榜' % board_id)
    board = Board.objects.filter(id=board_id).get()
    if board.type == 'max_three':
        for item in board.boarditem_set.all():
            item.max_rating, item.times = _get_max_rating(item.cf_user.handle, board.start_time, board.end_time,
                                                          3)
            item.max_rating = int(item.max_rating / 3.0)
            if item.times < 5:
                item.max_rating = int(item.max_rating * 0.9)
            item.save()
    else:
        for item in board.boarditem_set.all():
            item.max_rating, item.times = _get_max_rating(item.cf_user.handle, board.start_time, board.end_time)
            item.old_rating = (_get_max_rating(item.cf_user.handle, datetime.datetime.fromtimestamp(100000),
                                               board.start_time))[0]
            if item.old_rating == 0:
                item.old_rating = 1500
            item.save()


def update_user_and_cf_user():
    for user in User.objects.all():
        cf_user = CFUser.objects.filter(handle=user.handle).first()
        if cf_user:
            cf_user.user = user
            cf_user.save()
