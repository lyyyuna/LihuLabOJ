from django.shortcuts import render
from django.contrib import auth

from rest_framework.views import APIView

from serializers import UserLoginSerializer
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
                        request=request
                        username=data['username']
                        password=data['password'])
            if user is not None:
                auth.login(request, user)
                shortcuts.success_response('Login success.')
            else:
                shortcuts.error_response('Login failed.')
        else:
            shortcuts.error_response('The input cannot be accepted.')