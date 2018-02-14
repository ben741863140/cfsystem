from board import utility
from board.models import CFUser, RatingChange


def update_rating():
    for user in CFUser.objects.all():
        res = utility.get_rating(user.handle)
        if res['status'] != 'OK':
            print('<update-rating> handle', user.handle, '不存在')
            continue
        user.rating = res['rating']
        user.save()


def update_rating_change():
    days_ago = [180, 90, 30, 14]
    for user in CFUser.objects.all():
        res = utility.get_rating_change(user, *days_ago)
        if len(RatingChange.objects.filter(cf_user_id=user.id)) == 0:
            for day in days_ago:
                RatingChange.objects.create(cf_user_id=user.id, days_ago=day)
        queryset = RatingChange.objects.filter(cf_user_id=user.id)

        for day in days_ago:
            rating_change = queryset.filter(days_ago=day).get()
            rating_change.oldRating = res[day]
            rating_change.newRating = res['newRating']
            rating_change.save()
