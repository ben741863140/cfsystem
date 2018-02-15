from django.db import models
from logreg.models import User


class CFUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
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
