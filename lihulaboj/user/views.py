from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.models import User, AnonymousUser

from rest_framework.views import APIView

from .serializers import UserLoginSerializer

from common import shortcuts, status


class UserLoginAPIView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            user = auth.authenticate(
                request=request,
                username=data['username'],
                password=data['password']
            )
            if user is not None:
                auth.login(request, user)
                return shortcuts.success_response(status.LOGIN_SUCCESS)
            else:
                return shortcuts.error_response(status.LOGIN_FAILED)
        else:
            return shortcuts.error_response(status.INPUT_INVALID)
