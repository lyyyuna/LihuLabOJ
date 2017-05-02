from django.conf.urls import url
from .views import UserLoginAPIView, UserLogoutAPIView

urlpatterns = [
    url(r'^login', UserLoginAPIView.as_view(), name='user_login_api'),
    url(r'^logout', UserLogoutAPIView.as_view(), name='user_logout_api')
]