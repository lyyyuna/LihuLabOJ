from django.shortcuts import render
from django.contrib import auth

from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import UserLoginSerializer
from common import shortcuts


class UserLoginAPIView(APIView):
    def post(self, request):
        '''
        For user login
        '''
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            user = auth.authenticate(
                        request=request,
                        username=data['username'],
                        password=data['password'])
            if user is not None:
                auth.login(request, user)
                return shortcuts.success_response('Login success.')
            else:
                return shortcuts.error_response('Login failed.')
        else:
            return shortcuts.error_response('The input cannot be accepted.')


class UserLogoutAPIView(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        '''
        For user logout
        '''
        auth.logout(request)
        return shortcuts.success_response('Logout success.')