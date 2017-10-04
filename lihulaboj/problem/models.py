from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Problem(models.Model):
    title = models.CharField(max_length=30, default='error')
    slug = models.SlugField(default='error')
    content = models.TextField(default='error')


class Answser(models.Model):
    createtime = models.DateTimeField(default=timezone.now)
    problem = models.ForeignKey(Problem, blank=True, null=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    result = models.CharField(default='error')
    is_pass = models.CharField(default='error')