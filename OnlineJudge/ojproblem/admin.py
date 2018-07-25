# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

class OJProblemModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'create_time', 'pass_num', 'total_num',)
    search_fields = ('id',)


class OJAnswerModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'update_time', 'problem', 'submitter', 'status', 'result')
    search_fields = ('id',)


class OJUserAnswerAggrModelAdmin(admin.ModelAdmin):
    list_display = ('result', 'update_time', 'problem', 'submitter')
    search_fields = ('submitter',)


admin.site.register(OJProblem, OJProblemModelAdmin)
admin.site.register(OJUserAnswerAggr, OJUserAnswerAggrModelAdmin)
admin.site.register(OJAnswer, OJAnswerModelAdmin)