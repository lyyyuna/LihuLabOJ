from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Problem(models.Model):
    title = models.CharField(max_length=30, default='error')
    slug = models.SlugField(default='error', unique=True)
    content = models.TextField(default='error')
    create_time = models.DateTimeField(auto_now_add=True)
    max_cpu_time = models.IntegerField(default=300)
    max_memory = models.IntegerField(default=64)
    input1 = models.TextField(default='error')
    output1 = models.TextField(default='error')
    input2 = models.TextField(default='error')
    output2 = models.TextField(default='error')
    pass_num = models.IntegerField(default=0)
    total_num = models.IntegerField(default=0)

    def __str__(self):
        return self.slug


class Answser(models.Model):
    STATUS = (
        ('pending', 'pending'),
        ('started', 'started'),
        ('finished', 'finished'),
        ('failed', 'failed'),
    )

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    problem = models.ForeignKey(Problem, blank=True, null=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    status = models.CharField(choices=STATUS, max_length=20)
    source_code = models.TextField(default='error')
    language = models.IntegerField(default=0)
    result = models.IntegerField(default=-1)
    cpu_time = models.IntegerField(default=0)
    memory = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        super(Answser, self).save(*args, **kwargs)
        if self.status == 'pending':
            from .tasks import judge
            max_cpu_time = self.problem.max_cpu_time
            max_memory = self.problem.memory * 1024 * 1024
            judge.delay(answer_id=self.id, source_code=self.source_code, language=self.language, max_cpu_time=max_cpu_time, max_memory=max_memory, test_case_id=self.problem.slug)
