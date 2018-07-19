from django.conf.urls import url, include
from rest_framework import routers
from .views import *


problem_list = OJProblemViewSet.as_view({
    'get' : 'list',
})

problem_detail = OJProblemViewSet.as_view({
    'get' : 'retrieve',
})


urlpatterns = [
    url(r'^all$', problem_list, name='problem_list_api'),
    url(r'^(?P<pk>[0-9]+)/detail', problem_detail, name='problem_detail_api'),
]