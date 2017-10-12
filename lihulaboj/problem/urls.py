from django.conf.urls import url, include
from rest_framework import routers
from .views import AnswserViewSet


router = routers.DefaultRouter()
router.register(r'submission', AnswserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]