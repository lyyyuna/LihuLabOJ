# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-26 14:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ojproblem', '0004_auto_20180726_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='ojanswer',
            name='runtime',
            field=models.IntegerField(default=-10),
        ),
    ]