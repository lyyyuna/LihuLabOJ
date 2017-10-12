# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-12 08:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('pending', 'pending'), ('started', 'started'), ('finished', 'finished'), ('failed', 'failed')], max_length=20)),
                ('source_code', models.TextField(default='eror')),
                ('language', models.CharField(default='c', max_length=10)),
                ('result', models.CharField(choices=[('N/A', 'N/A'), ('WRONG_ANSWER', 'WRONG_ANSWER'), ('SUCCESS', 'SUCCESS'), ('CPU_TIME_LIMIT_EXCEEDED', 'CPU_TIME_LIMIT_EXCEEDED'), ('REAL_TIME_LIMIT_EXCEEDED', 'REAL_TIME_LIMIT_EXCEEDED'), ('MEMORY_LIMIT_EXCEEDED', 'MEMORY_LIMIT_EXCEEDED'), ('RUNTIME_ERROR', 'RUNTIME_ERROR'), ('SYSTEM_ERROR', 'SYSTEM_ERROR')], max_length=20)),
                ('real_time', models.IntegerField(default=0)),
                ('memory', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='error', max_length=30)),
                ('slug', models.SlugField(default='error')),
                ('content', models.TextField(default='error')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('max_cpu_time', models.IntegerField(default=1500)),
                ('max_memory', models.IntegerField(default=128)),
            ],
        ),
    ]
