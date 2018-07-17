from django.conf.urls import url
from .views import *
from rest_framework import routers


urlpatterns = [
    url(r'^login$', UserLoginAPIView.as_view(), name='user_login_api'),
    url(r'^logout$', UserLogoutAPIView.as_view(), name='user_logout_api'),
    url(r'^register$', UserRegisterAPIView.as_view(), name='user_register_api'),
]