from django.db import models
from logreg.models import User
from django.conf import settings


class CFUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    handle = models.CharField(max_length=30, unique=True)
    rating = models.IntegerField(default=0)
    last_update = models.DateTimeField(auto_now=True)
    realname = models.CharField(max_length=5, default='')


class RatingChange(models.Model):
    newRating = models.IntegerField()
    ratingUpdateTimeSeconds = models.IntegerField(primary_key=True)
    cf_user = models.ForeignKey(CFUser, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'board_ratingchange'
        unique_together = (('cf_user', 'ratingUpdateTimeSeconds'),)


class Board(models.Model):
    name = models.CharField(max_length=20)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    type = models.CharField(max_length=20)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)


class BoardItem(models.Model):
    cf_user = models.ForeignKey(CFUser, on_delete=models.PROTECT)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    max_rating = models.IntegerField()
    old_rating = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    times = models.IntegerField(default=0)
