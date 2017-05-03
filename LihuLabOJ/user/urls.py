from django.conf.urls import url
from .views import UserLoginAPIView, UserLogoutAPIView, UserProfileAPIView

urlpatterns = [
    url(r'^login', UserLoginAPIView.as_view(), name='user_login_api'),
    url(r'^logout', UserLogoutAPIView.as_view(), name='user_logout_api'),
    url(r'^profile/(\d+)', UserProfileAPIView.as_view(), name='user_profile_api')
]