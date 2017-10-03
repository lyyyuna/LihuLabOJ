from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    signature = models.CharField(max_length=20, default='')


class Invitation(models.Model):
    code = models.CharField(max_length=20, default='error')