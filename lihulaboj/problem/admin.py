from django.contrib import admin
from .models import Problem, Answser


class ProblemModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug',)
    search_fields = ('slug',)


class AnswerModelAdmin(admin.ModelAdmin):
    list_display = ('create_time', 'author', 'problem')


admin.site.register(Problem, ProblemModelAdmin)
admin.site.register(Answser, AnswerModelAdmin)
