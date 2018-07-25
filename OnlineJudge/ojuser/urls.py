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
user_rank_list = OJUserRanksViewSet.as_view({
    'get' : 'list',
})

urlpatterns = [
    url(r'^login$', UserLoginAPIView.as_view(), name='user_login_api'),
    url(r'^logout$', UserLogoutAPIView.as_view(), name='user_logout_api'),
    url(r'^register$', UserRegisterAPIView.as_view(), name='user_register_api'),
    url(r'^profile/my$', user_detail, name='user_myprofile_api'),
    url(r'^profile/my/update$', edit_user_detail, name='edit_user_profile_api'),
    url(r'^profile/my/password$', change_user_pw, name='change_user_password_api'),
    url(r'^ranks$', user_rank_list, name='user_rank_list_api'),
]