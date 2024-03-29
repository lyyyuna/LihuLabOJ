# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *


class ActiviationCodeModelAdmin(admin.ModelAdmin):
    list_display = ('key', 'count',)


class UserProfileModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'signature', 'pass_num', 'total_num', 'last_submit_time',)


admin.site.register(ActiviationCode, ActiviationCodeModelAdmin)
admin.site.register(OJUserProfile, UserProfileModelAdmin)