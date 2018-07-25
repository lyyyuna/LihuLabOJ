# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import User, AnonymousUser

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from .serializers import *
from common.shortcuts import *
from .models import *


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
                return successResponse('login success')
            else:
                return errorResponse('username or password not right')
        else:
            return errorResponse('input invalid')


class UserLogoutAPIView(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        auth.logout(request)
        return successResponse('logout success')


class UserRegisterAPIView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            userkey = data['activiation_code']
            ackey_queryset = ActiviationCode.objects.all()
            for ackey in ackey_queryset:
                if userkey == ackey.key:
                    if User.objects.filter(username=data['username']).exists():
                        return errorResponse('username already exists')
                    u = User.objects.create_user(username=data['username'], 
                                             password=data['password'])
                    OJUserProfile.objects.create(user=u)
                    return successResponse('register success')
                else:
                    continue
            # if run here, means userkey != ackey
            return errorResponse('wrong ac key')
        else:
            return errorResponse('input invalid')


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action == 'update':
            self.permission_classes = [IsAuthenticated,]
        elif self.action == 'change_password':
            self.permission_classes = [IsAuthenticated,]
        elif self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated,]
        return super(self.__class__, self).get_permissions()

    def retrieve(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return successResponse(serializer.data)

    def update(self, request):
        user = request.user
        serializer = UserProfileUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return successResponse('update profile success')
        else:
            return errorResponse('input invalid')

    def change_password(self, request):
        user = request.user
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.data['password'])
            user.save()
            return successResponse('update password success')
        else:
            return errorResponse('input invalid')


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'


class OJUserRanksViewSet(viewsets.ModelViewSet):
    queryset = OJUserProfile.objects.all().order_by('-pass_num', 'total_num')
    pagination_class = StandardResultsSetPagination
    serializer_class = UserRankSerializer