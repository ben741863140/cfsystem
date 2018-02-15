from board import utility
from board.models import CFUser, RatingChange
import datetime


def update_rating():
    for user in CFUser.objects.all():
        res = utility.get_rating(user.handle)
        if res['status'] != 'OK':
            print('<update-rating> handle', user.handle, '不存在')
            continue
        user.rating = res['rating']
        user.save()


def get_result_for_days(raw, *days_ago):
    res = {}
    now_rating = 0
    for info in raw:
        now_rating = info['newRating']
        update_time = datetime.datetime.fromtimestamp(info['ratingUpdateTimeSeconds'])
        # 得到的results['result']是按时间轴从以前到现在，所以遇到第一个满足条件的就是oldRating，只写进一次
        for day in filter(lambda x: x if x not in res.keys() else None, days_ago):
            if (datetime.datetime.now() - update_time).days <= day:
                res[day] = info['oldRating']
    res['newRating'] = now_rating
    for day in filter(lambda x: x if x not in res.keys() else None, days_ago):
        res[day] = now_rating
    return res


def update_rating_change():
    days_ago = [180, 90, 30, 14]
    for user in CFUser.objects.all():
        result = utility.get_rating_change(user.handle)
        queryset = RatingChange.objects.filter(cf_user__id=user.id)
        for change in result:
            if len(queryset.filter(ratingUpdateTimeSeconds=change['ratingUpdateTimeSeconds'])) == 0:
                queryset.create(ratingUpdateTimeSeconds=change['ratingUpdateTimeSeconds'],
                                oldRating=change['oldRating'],
                                newRating=change['newRating'],
                                cf_user_id=user.id)
        res = get_result_for_days(result, *days_ago)
        for day in days_ago:
            if len(queryset.filter(days_ago=day)) == 0:
                RatingChange.objects.create(cf_user_id=user.id, days_ago=day)
            rating_change = queryset.filter(days_ago=day).get()
            rating_change.oldRating = res[day]
            rating_change.newRating = res['newRating']
            rating_change.save()
