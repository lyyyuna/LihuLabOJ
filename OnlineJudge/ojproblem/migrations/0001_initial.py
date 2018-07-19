# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-19 02:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OJAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(default='pending', max_length=20)),
                ('source_code', models.CharField(max_length=2048)),
                ('result', models.IntegerField(default=-1)),
                ('raw_result', models.CharField(max_length=2048)),
                ('cpu', models.IntegerField(default=-1)),
                ('memory', models.IntegerField(default=-1)),
            ],
        ),
        migrations.CreateModel(
            name='OJProblem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='error', max_length=30)),
                ('content', models.TextField(default='error')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('input1', models.TextField(default='error')),
                ('output1', models.TextField(default='error')),
                ('input2', models.TextField(default='error')),
                ('output2', models.TextField(default='error')),
                ('pass_num', models.IntegerField(default=0)),
                ('total_num', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='OJUserAnswerAggr',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.IntegerField(default=-1)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('submit_time', models.IntegerField(default=0)),
                ('problem', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ojproblem.OJProblem')),
                ('submitter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='ojanswer',
            name='problem',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ojproblem.OJProblem'),
        ),
        migrations.AddField(
            model_name='ojanswer',
            name='submitter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]