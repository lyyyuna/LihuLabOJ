# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-25 13:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ojproblem', '0002_auto_20180725_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ojanswer',
            name='cpu',
            field=models.IntegerField(db_index=True, default=-1),
        ),
        migrations.AlterField(
            model_name='ojanswer',
            name='memory',
            field=models.IntegerField(db_index=True, default=-1),
        ),
    ]