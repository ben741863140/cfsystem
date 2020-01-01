# _*_ utf-8 _*_
from django.db import models
from django.contrib.auth.models import AbstractUser


class Pair(object):
    def __init__(self, num, str):
        self.val = num
        self.tag = str


class User(AbstractUser):
    Choices = []
    for i in range(1, 99):
        if i < 10:
            Choices.append(Pair(i, '0' + str(i)))
        else:
            Choices.append(Pair(i, str(i)))
    grade_choices = [(choice.val, choice.tag) for choice in Choices]
    nickname = models.CharField(max_length=20, blank=True, verbose_name='昵称', help_text='<ul><li>可不填</li></ul>')
    realname = models.CharField(max_length=10, blank=False, verbose_name='真名', help_text='<ul><li>必填</li></ul>',
                                error_messages={'blank': '不能为空'})
    handle = models.CharField(max_length=20, blank=False, verbose_name='CF账号', help_text='<ul><li>必填</li></ul>',
                              error_messages={'unique': '账号已存在'}, unique=True)
    grade = models.IntegerField(verbose_name='年级', help_text='<ul><li>必填</li></ul>',
                                error_messages={'blank': '不能为空'}, choices=grade_choices, default=16, blank=False)

    # Unknown what's Meta
    class Meta(AbstractUser.Meta):
        pass

    # def set_password(self, raw_password):
    #     self.password = make_password(raw_password)


class Captcha(models.Model):
    username = models.CharField(max_length=150, blank=False)
    handle = models.CharField(max_length=20, blank=False)
    update_time = models.DateTimeField()
    captcha = models.CharField(max_length=200, blank=False)
    status = models.IntegerField(default=0)
