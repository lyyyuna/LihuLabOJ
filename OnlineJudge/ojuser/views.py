# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import User, AnonymousUser

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

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
                    User.objects.create_user(username=data['username'], password=data['password'])
                    return successResponse('register success')
                else:
                    continue
            # if run here, means userkey != ackey
            return errorResponse('wrong ac key')
        else:
            return errorResponse('input invalid')