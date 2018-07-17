# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *


class ActiviationCodeModelAdmin(admin.ModelAdmin):
    list_display = ('key',)


admin.site.register(ActiviationCode, ActiviationCodeModelAdmin)
