from django.conf.urls import url
from .views import UserLoginAPIView, UserLogoutAPIView, UserProfileViewSet
from rest_framework import routers


user_list = UserProfileViewSet.as_view({
    'get' : 'list',
})
user_detail = UserProfileViewSet.as_view({
    'get' : 'retrieve',
})


urlpatterns = [
    url(r'^login', UserLoginAPIView.as_view(), name='user_login_api'),
    url(r'^logout', UserLogoutAPIView.as_view(), name='user_logout_api'),
    url(r'^allprofile', user_list, name='user_allprofile_api'),
    url(r'^profile/my', user_detail, name='user_myprofile_api'),
]