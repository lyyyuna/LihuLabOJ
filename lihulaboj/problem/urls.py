from django.conf.urls import url, include
from rest_framework import routers
from .views import AnswserViewSet, ProblemViewSet


router = routers.DefaultRouter()
router.register(r'submission', AnswserViewSet)

problem_list = ProblemViewSet.as_view({
    'get' : 'list',
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

urlpatterns = [
    #url(r'^', include(router.urls)),
    url(r'^admin/create', create_problem, name='create_problem_api'),
    url(r'^all', problem_list, name='problem_list_api'),
    url(r'^admin/(?P<pk>[0-9]+)/update/', update_problem, name='update_problem_api'),
    url(r'^admin/(?P<pk>[0-9]+)/delete/', delete_problem, name='delete_problem_api'),
]