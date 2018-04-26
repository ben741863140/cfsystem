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
    name = models.CharField(max_length=20)
    effective_time = models.DateTimeField(default=0)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    type = models.CharField(max_length=20)


class BoardItem(models.Model):
    cf_user = models.ForeignKey(CFUser, on_delete=models.PROTECT)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    max_rating = models.IntegerField()
    oldRating = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
