from django.db import models
from logreg.models import User
from django.conf import settings


class CFUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    handle = models.CharField(max_length=30, unique=True)
    rating = models.IntegerField(default=0)
    last_update = models.DateTimeField(auto_now=True)
    realname = models.CharField(max_length=5, default='')


class RatingChange(models.Model):
    cf_user = models.ForeignKey(CFUser, on_delete=models.CASCADE)
    days_ago = models.IntegerField(null=True)
    oldRating = models.IntegerField(default=0)
    newRating = models.IntegerField(default=0)
    last_update = models.DateTimeField(auto_now=True)
    ratingUpdateTimeSeconds = models.IntegerField(null=True)


class Board(models.Model):
    cf_user = models.ManyToManyField(CFUser)


# class DynamicBoard(Board): # 暂时不加
#     days_ago = models.IntegerField()


class StaticBoard(Board):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


class RatingStaticBoard(StaticBoard):
    rating = models.IntegerField()


class RatingChangeStaticBoard(StaticBoard):
    old_rating = models.IntegerField()
    new_rating = models.IntegerField()
