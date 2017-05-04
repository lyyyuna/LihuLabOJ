from django.conf.urls import url
from .views import UserLoginAPIView, UserLogoutAPIView, UserProfileAPIView,\
         EditUserProfileAPIView

urlpatterns = [
    url(r'^login', UserLoginAPIView.as_view(), name='user_login_api'),
    url(r'^logout', UserLogoutAPIView.as_view(), name='user_logout_api'),
    url(r'^profile/(\d+)', UserProfileAPIView.as_view(), name='user_profile_api'),
    url(r'^editprofile', EditUserProfileAPIView.as_view(), name='edit_user_profile_api')
]