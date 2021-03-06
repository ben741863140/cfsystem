from board import utility
from board.models import CFUser, RatingChange, User
from logreg.models import Captcha
from .models import Board
import datetime
from .get_handle import get_handle


def captcha_clean():
    now = datetime.datetime.now() - datetime.timedelta(minutes=30)
    for item in Captcha.objects.all():
        print(item.handle)
        if item.update_time.__lt__(now):
            try:
                item.delete()
            except Exception:
                continue


def cf_handle_update():
    for user in User.objects.all():
        temp = get_handle(user.handle)
        print(temp + '  ' + user.handle)
        if user.handle != temp:
            user.handle = temp
            user.save()
            try:
                cf_user = CFUser.objects.get(user_id=user.id)
                cf_user.handle = temp
                cf_user.grade = user.grade
                cf_user.save()
            except Exception:
                continue


def update_rating(handle=''):
    def update(cf_user):
        res = utility.get_rating(get_handle(cf_user.handle))
        if res['status'] != 'OK':
            print('<update-rating> handle', cf_user.handle, '不存在')
            return
        cf_user.rating = res['rating']
        cf_user.save()

    if handle:
        update(CFUser.objects.filter(handle=handle).get())
    else:
        i = 0
        for user in CFUser.objects.all():
            update(user)
            i += 1
            # print('update rating [%d/%d]' % (i, size))


def update_rating_change(handle=''):
    # 更新 cf_user 的RatingChange
    def update(cf_user):
        result = utility.get_rating_change(get_handle(cf_user.handle))
        if result['status'] != 'OK':
            print(result['comment'])
            return
        result = result['result']
        result = result[RatingChange.objects.filter(cf_user_id=cf_user.id).count():]
        for change in result:
            RatingChange.objects.get_or_create(ratingUpdateTimeSeconds=change['ratingUpdateTimeSeconds'],
                                               newRating=change['newRating'],
                                               cf_user_id=cf_user.id)

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


def _get_times(handle, start_time, end_time):  # 获得参加比赛场次
    count = 0
    for rc in RatingChange.objects.filter(cf_user__handle=handle).all():
        time = datetime.datetime.fromtimestamp(rc.ratingUpdateTimeSeconds)
        if start_time <= time < end_time:
            count += 1
    return count


def update_board(board_id=-1):  # -1表示更新所有Board
    if board_id == -1:
        for board in Board.objects.all():
            update_board(board.id)
        return
    # print('更新ID为%d的榜' % board_id)
    board = Board.objects.filter(id=board_id).get()
    if board.type == 'rating':
        for item in board.boarditem_set.all():
            cf_user = item.cf_user
            item.max_rating = cf_user.rating
            # print(cf_user.handle, cf_user.rating)
            item.times = _get_times(cf_user.handle, board.start_time, board.end_time)
            item.save()
    elif board.type == 'max_three':
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


# 将cf_user和user关联起来，因为user只存了handle，所以对应的cf_user可能没对应到user上
# 需修改数据库结构解决
def update_user_and_cf_user():
    for user in User.objects.all():
        cf_user = None
        try:
            cf_user = CFUser.objects.filter(handle=user.handle).first()
        except Exception:
            cf_user = None
        if cf_user is not None:
            cf_user.user = user
            cf_user.handle = user.handle
            cf_user.grade = user.grade
            cf_user.save()
