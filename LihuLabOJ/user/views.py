from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from .serializers import UserLoginSerializer, UserProfileSerializer
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


class UserProfileAPIView(APIView):
    def get(self, request, id):
        '''
        View a user's profile
        '''
        try:
            user = User.objects.get(pk=id)
        except User.DoesNotExist:
            return shortcuts.error_response('The user doesnt exist.')

        profile = UserProfileSerializer(user)
        return shortcuts.success_response(profile.data)


class EditUserProfileAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        '''
        Update a user's profile
        '''
        user = request.user
        if user is not None:
            profile = UserProfileSerializer(user, data=request.data, partial=True)
            if profile.is_valid():
                profile.save()
            else:
                return shortcuts.error_response('The input is invalid.')
            return shortcuts.success_response('Update user profile success.')
        else:
            return shortcuts.error_response('The user doesnt exist.')
