# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-26 14:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ojproblem', '0005_ojanswer_runtime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ojanswer',
            name='raw_result',
            field=models.TextField(),
        ),
    ]
