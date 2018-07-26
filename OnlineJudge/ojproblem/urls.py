from django.conf.urls import url, include
from rest_framework import routers
from .views import *


problem_list = OJProblemViewSet.as_view({
    'get' : 'list',
})

problem_detail = OJProblemViewSet.as_view({
    'get' : 'retrieve',
})

answer_detail = OJAnswerViewSet.as_view({
    'get' : 'retrieve',
})

answer_list = OJAnswerViewSet.as_view({
    'get' : 'myanswers',
})

answer_rank_list = OJRanksViewSet.as_view({
    'get' : 'ranks',
})

submit_answer = OJAnswerViewSet.as_view({
    'post' : 'submit',
})


urlpatterns = [
    url(r'^all$', problem_list, name='problem_list_api'),
    url(r'^(?P<pk>[0-9]+)/detail', problem_detail, name='problem_detail_api'),
    url(r'^answer/(?P<pk>[0-9]+)/detail', answer_detail, name='answer_detail_api'),
    url(r'^(?P<pk>[0-9]+)/myanswers', answer_list, name='problem_myanswer_list_api'),
    url(r'^(?P<pk>[0-9]+)/ranks', answer_rank_list, name='problem_rank_list_api'),
    url(r'^(?P<pk>[0-9]+)/submit', submit_answer, name='submit_answer_api'),
]