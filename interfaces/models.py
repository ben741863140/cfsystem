from django.db import models


class OJUser(models.Model):
    username = models.CharField(max_length=20, blank=False, unique=True)
    password = models.CharField(max_length=200, blank=False)
    is_super = models.BooleanField(default=False)
    cf_handle = models.CharField(max_length=20, blank=True, unique=True)
    is_active = models.BooleanField(default=False)
