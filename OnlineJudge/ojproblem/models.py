# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class OJProblem(models.Model):
    title = models.CharField(max_length=30, default='error')
    content = models.TextField(default='error')
    create_time = models.DateTimeField(auto_now_add=True)
    input1 = models.TextField(default='error')
    output1 = models.TextField(default='error')
    input2 = models.TextField(default='error')
    output2 = models.TextField(default='error')
    pass_num = models.IntegerField(default=0)
    total_num = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)


class OJAnswer(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    problem = models.ForeignKey(OJProblem, blank=True, null=True, on_delete=models.SET_NULL)
    submitter = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, default='pending')
    source_code = models.TextField(max_length=2048)
    result = models.IntegerField(default=-1)
    raw_result = models.CharField(max_length=2048)
    cpu = models.IntegerField(default=-1, db_index=True)
    memory = models.IntegerField(default=-1, db_index=True)

    def __str__(self):
        return str(self.id)


class OJUserAnswerAggr(models.Model):
    result = models.IntegerField(default=-1)
    update_time = models.DateTimeField(auto_now=True)
    problem = models.ForeignKey(OJProblem, blank=True, null=True, on_delete=models.SET_NULL)
    answer = models.ForeignKey(OJAnswer, blank=True, null=True, on_delete=models.SET_NULL)
    submitter = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    cpu = models.IntegerField(default=-1)
    memory = models.IntegerField(default=-1)
