from django.conf.urls import url
from .views import *
from rest_framework import routers


user_detail = UserProfileViewSet.as_view({
    'get' : 'retrieve',
})
edit_user_detail = UserProfileViewSet.as_view({
    'post' : 'update',
})
change_user_pw = UserProfileViewSet.as_view({
    'post' : 'change_password',
})

urlpatterns = [
    url(r'^login$', UserLoginAPIView.as_view(), name='user_login_api'),
    url(r'^logout$', UserLogoutAPIView.as_view(), name='user_logout_api'),
    url(r'^register$', UserRegisterAPIView.as_view(), name='user_register_api'),
]