# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class OJUserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    signature = models.CharField(max_length=20, default='')


class ActiviationCode(models.Model):
    key = models.CharField(max_length=20, default='error')
