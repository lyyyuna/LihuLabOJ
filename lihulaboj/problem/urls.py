from django.conf.urls import url, include
from rest_framework import routers
from .views import AnswserViewSet, ProblemViewSet


problem_list = ProblemViewSet.as_view({
    'get' : 'list',
})

problem_detail = ProblemViewSet.as_view({
    'get' : 'detail',
})

create_problem = ProblemViewSet.as_view({
    'post' : 'edit',
})

update_problem = ProblemViewSet.as_view({
    'post' : 'update',
})

delete_problem = ProblemViewSet.as_view({
    'post' : 'delete'
})

submit_answer = AnswserViewSet.as_view({
    'post' : 'submit'
})

answer_status = AnswserViewSet.as_view({
    'get' : 'status'
})

urlpatterns = [
    url(r'^all', problem_list, name='problem_list_api'),
    url(r'^(?P<pk>[0-9]+)/detail', problem_detail, name='problem_detail_api'),
    url(r'^admin/create', create_problem, name='create_problem_api'),
    url(r'^admin/(?P<pk>[0-9]+)/update/', update_problem, name='update_problem_api'),
    url(r'^admin/(?P<pk>[0-9]+)/delete/', delete_problem, name='delete_problem_api'),
    url(r'(?P<problem_id>[0-9]+)/submit', submit_answer, name='submit_answer_api'),
    url(r'^answer/(?P<answer_id>[0-9]+)/status', answer_status, name='answer_status_api'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]