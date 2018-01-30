# _*_ utf-8 _*_
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(max_length=20, blank=True, verbose_name='昵称',help_text='<ul><li>可不填</li></ul>')
    realname = models.CharField(max_length=10, blank=False, verbose_name='真名',help_text='<ul><li>必填</li></ul>')
    handle = models.CharField(max_length=20, blank=False, verbose_name='CF账号',help_text='<ul><li>必填</li></ul>')

    # Unknown what's Meta
    class Meta(AbstractUser.Meta):
        pass
