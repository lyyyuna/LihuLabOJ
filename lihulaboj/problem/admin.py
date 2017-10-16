from django.contrib import admin
from .models import Problem


class ProblemModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug',)
    search_fields = ('slug',)


admin.site.register(Problem, ProblemModelAdmin)
