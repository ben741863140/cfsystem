from board import utility
from board.models import CFUser, RatingChange
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
            print('update rating [%d/%d]' % (i, size))


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


def update_rating_change(handle=''):
    days_ago = [180, 90, 30, 14]

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
        res = get_result_for_days(result, *days_ago)
        for day in days_ago:
            if len(queryset.filter(days_ago=day)) == 0:
                RatingChange.objects.create(cf_user_id=cf_user.id, days_ago=day)
            rating_change = queryset.filter(days_ago=day).get()
            rating_change.oldRating = res[day]
            rating_change.newRating = res['newRating']
            rating_change.save()

    if handle:
        update(CFUser.objects.filter(handle=handle).get())
    else:
        i = 0
        size = CFUser.objects.count()
        for user in CFUser.objects.all():
            update(user)
            i += 1
            print('update rating change [%d/%d]' % (i, size))
