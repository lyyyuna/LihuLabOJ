from django.conf.urls import url, include
from rest_framework import routers
from .views import *


problem_list = OJProblemViewSet.as_view({
    'get' : 'list',
})


urlpatterns = [
    url(r'^all$', problem_list, name='problem_list_api'),
]