from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Problem(models.Model):
    title = models.CharField(max_length=30, default='error')
    slug = models.SlugField(default='error')
    content = models.TextField(default='error')
    create_time = models.DateTimeField(auto_now_add=True)
    max_cpu_time = models.IntegerField(default=300)
    max_memory = models.IntegerField(default=64)
    input1 = models.TextField(default='error')
    output1 = models.TextField(default='error')
    input2 = models.TextField(default='error')
    output2 = models.TextField(default='error')


class Answser(models.Model):
    STATUS = (
        ('pending', 'pending'),
        ('started', 'started'),
        ('finished', 'finished'),
        ('failed', 'failed'),
    )

    RESULT = (
        ('N/A', 'N/A'),
        ('WRONG_ANSWER', 'WRONG_ANSWER'),
        ('SUCCESS', 'SUCCESS'),
        ('CPU_TIME_LIMIT_EXCEEDED', 'CPU_TIME_LIMIT_EXCEEDED'),
        ('REAL_TIME_LIMIT_EXCEEDED', 'REAL_TIME_LIMIT_EXCEEDED'),
        ('MEMORY_LIMIT_EXCEEDED', 'MEMORY_LIMIT_EXCEEDED'),
        ('RUNTIME_ERROR', 'RUNTIME_ERROR'),
        ('SYSTEM_ERROR', 'SYSTEM_ERROR')
    )

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    #problem = models.ForeignKey(Problem, blank=True, null=True, on_delete=models.SET_NULL)
    #author = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    status = models.CharField(choices=STATUS, max_length=20)
    source_code = models.TextField(default='error')
    language = models.CharField(default='c', max_length=10)
    result = models.TextField(default='error')
    cpu_time = models.IntegerField(default=0)
    memory = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        super(Answser, self).save(*args, **kwargs)
        if self.status == 'pending':
            from .tasks import judge
            judge.delay(answer_id=self.id, source_code=self.source_code)
