from django.conf.urls import url

from .views import AnnouncementList,AnnouncementDetail

urlpatterns = [
    url(r'^$', AnnouncementList.as_view(),name='announcement-list'),
    url(r'^(?P<pk>[0-9]+)/$', AnnouncementDetail.as_view(),name='announcement-detail'),
]