from django.conf.urls import url
from .views import UserLoginAPIView, UserRegisterAPIView, UserLogoutAPIView, UserProfileViewSet
from rest_framework import routers


user_list = UserProfileViewSet.as_view({
    'get' : 'list',
})
user_detail = UserProfileViewSet.as_view({
    'get' : 'retrieve',
})
edit_user_detail = UserProfileViewSet.as_view({
    'post' : 'update',
})
change_user_pw = UserProfileViewSet.as_view({
    'post' : 'change_password'
})
user_detail_by_id = UserProfileViewSet.as_view({
    'get' : 'retrieve_byid'
})
admin_change_user_pw = UserProfileViewSet.as_view({
    'post' : 'change_password_byid'
})
admin_update_user_profile = UserProfileViewSet.as_view({
    'post' : 'update_byid'
})


urlpatterns = [
    url(r'^login', UserLoginAPIView.as_view(), name='user_login_api'),
    url(r'^logout', UserLogoutAPIView.as_view(), name='user_logout_api'),
    url(r'^register', UserRegisterAPIView.as_view(), name='user_register_api'),
    url(r'^allprofile', user_list, name='user_allprofile_api'),
    url(r'^profile/my$', user_detail, name='user_myprofile_api'),
    url(r'^profile/my/update', edit_user_detail, name='edit_user_profile_api'),
    url(r'^profile/my/password', change_user_pw, name='change_user_password_api'),
    url(r'^profile/admin/(?P<pk>[0-9]+)$', user_detail_by_id, name='user_profile_by_id_api'),
    url(r'^profile/admin/(?P<pk>[0-9]+)/password', admin_change_user_pw, name='change_password_by_id_api'),
    url(r'^profile/admin/(?P<pk>[0-9]+)/update', admin_update_user_profile, name='update_byid_api'),
]