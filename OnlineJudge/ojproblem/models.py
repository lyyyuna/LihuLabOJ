# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


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


# method for updating
@receiver(post_save, sender=OJProblem)
def update_stock(sender, instance, **kwargs):
    post_save.disconnect(update_stock, sender=sender)
    input2 = instance.input2.splitlines()
    output2 = instance.output2.splitlines()
    instance.input2 = '\n'.join(input2)
    instance.output2 = '\n'.join(output2)
    instance.save()
    post_save.connect(update_stock, sender=sender)


class OJAnswer(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    problem = models.ForeignKey(OJProblem, blank=True, null=True, on_delete=models.SET_NULL)
    submitter = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, default='pending')
    source_code = models.TextField(max_length=2048)
    result = models.IntegerField(default=-10)
    raw_result = models.TextField()
    cpu = models.IntegerField(default=-1, db_index=True)
    memory = models.IntegerField(default=-1, db_index=True)
    runtime = models.IntegerField(default=-10)
    # WRONG_ANSWER = -1 (this means the process exited normally, but the answer is wrong)
    # SUCCESS = 0 (this means the answer is accepted)
    # CPU_TIME_LIMIT_EXCEEDED = 1
    # REAL_TIME_LIMIT_EXCEEDED = 2
    # MEMORY_LIMIT_EXCEEDED = 3
    # RUNTIME_ERROR = 4
    # SYSTEM_ERROR = 5
    def __str__(self):
        return str(self.id)


class OJUserAnswerAggr(models.Model):
    result = models.IntegerField(default=-1)
    update_time = models.DateTimeField(auto_now=True)
    problem = models.ForeignKey(OJProblem, blank=True, null=True, on_delete=models.SET_NULL, db_index=True)
    answer = models.ForeignKey(OJAnswer, blank=True, null=True, on_delete=models.SET_NULL, db_index=True)
    submitter = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, db_index=True)
    cpu = models.IntegerField(default=-1)
    memory = models.IntegerField(default=-1)