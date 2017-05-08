from django.conf.urls import url
from .views import UserLoginAPIView, UserLogoutAPIView
from .views import UserProfileViewSet, AdminUserProfileViewSet, RankListViewSet
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
set_password = UserProfileViewSet.as_view({
    'post' : 'set_password',
})
get_myprofile = UserProfileViewSet.as_view({
    'post' : 'get_myprofile',
})
admin_edit_user_detail = AdminUserProfileViewSet.as_view({
    'post' : 'update'
})
admin_set_user_password = AdminUserProfileViewSet.as_view({
    'post' : 'set_password'
})
get_ranklist = RankListViewSet.as_view({
    'get' : 'list',
})


urlpatterns = [
    url(r'^login', UserLoginAPIView.as_view(), name='user_login_api'),
    url(r'^logout', UserLogoutAPIView.as_view(), name='user_logout_api'),
    url(r'^allprofile', user_list, name = 'user_allprofile_api'),
    url(r'^profile/(?P<pk>[0-9]+)', user_detail, name = 'user_profile_api'),
    url(r'^profile', edit_user_detail, name = 'edit_user_profile_api'),
    url(r'^changepw', set_password, name='user_change_password_api'),
    url(r'^myprofile', get_myprofile, name='user_get_self_profile_api'),
    url(r'^admin/profile/(?P<pk>[0-9]+)', admin_edit_user_detail, name = 'admin_edit_user_profile_api'),
    url(r'^admin/changepw/(?P<pk>[0-9]+)', admin_set_user_password, name = 'admin_set_user_password_api'),
    url(r'^rank', get_ranklist, name='get_ranklist_api')
]
