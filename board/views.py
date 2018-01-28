from django.shortcuts import render
from board import utility
from board.models import CFUser, RatingChange
from django.http.response import HttpResponse


def update_rating():
    handles = []
    for user in CFUser.objects.all():
        handles.append(user.handle)
    res = utility.get_rating(*handles)
    for user in CFUser.objects.all():
        user.rating = res[user.handle]
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


def load_cf_user():
    for handle in open('cf.txt', 'r').readlines():
        handle = handle.strip().lower()
        if len(CFUser.objects.filter(handle=handle)) == 0:
            CFUser.objects.create(handle=handle)


def test_page(request):
    return HttpResponse('test')


update_rating()
