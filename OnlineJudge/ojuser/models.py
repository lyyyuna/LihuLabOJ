# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class OJUserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ojuserprofile')
    signature = models.CharField(max_length=20, default='')
    pass_num = models.IntegerField(default=0, db_index=True)
    total_num = models.IntegerField(default=0, db_index=True)
    last_submit_time = models.DateTimeField(auto_now_add=True)


class ActiviationCode(models.Model):
    key = models.CharField(max_length=20, default='error')
    count = models.IntegerField(default=10)
