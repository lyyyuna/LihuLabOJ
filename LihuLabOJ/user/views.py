from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import User, AnonymousUser

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes, detail_route

from .serializers import UserLoginSerializer, UserProfileSerializer, PasswordSerializer, \
                    AdminUserProfileSerializer, RankListSerializer
from .models import UserProfile
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


# Pagination
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    pagination_class = StandardResultsSetPagination
    serializer_class = UserProfileSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated,]            
        return super(UserProfileViewSet, self).get_permissions()

    # def list(self, request):
    #     queryset = User.objects.all().order_by('id')
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = UserProfileSerializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #     else:
    #         serializer = UserProfileSerializer(queryset, many=True)
    #         return Response(serializer.data)

    def retrieve(self, request, pk):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        profile = UserProfileSerializer(user)
        return shortcuts.success_response(profile.data)

    def update(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return shortcuts.success_response('Update user profile success.')
        else:
            return shortcuts.error_response(serializer.errors)

    def set_password(self, request):
        user = request.user
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.data['password'])
            user.save()
            return shortcuts.success_response('Set password success.')
        else:
            return shortcuts.error_response(serializer.errors)

    def get_myprofile(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return shortcuts.success_response(serializer.data)
        
        
class AdminUserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser,]            
        return super(AdminUserProfileViewSet, self).get_permissions()

    def update(self, request, pk):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = AdminUserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return shortcuts.success_response('Admin: Update user profile success.')
        else:
            return shortcuts.error_response(serializer.errors)

    def set_password(self, request, pk):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.data['password'])
            user.save()
            return shortcuts.success_response('Admin: Set password success.')
        else:
            return shortcuts.error_response(serializer.errors)

    def set_user_status(self, request, pk, status):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        if user.is_staff == True:
            return shortcuts.error_response('This user is admin. Cannot set status.')
        else:
            if status == 1:
                if user.is_active == True:
                    return shortcuts.success_response('User already enabled.')
                else:
                    user.is_active = True
                    user.save()
                    return shortcuts.success_response('Enable user success.')
            if status == 0:
                if user.is_active == True:
                    user.is_active = False
                    user.save()
                    return shortcuts.success_response('Disable user success.')
            else:
                return shortcuts.error_response('Unkown status.')

class RankListViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all().order_by('-passproblem', 'failedproblem', 'id')
    pagination_class = StandardResultsSetPagination
    serializer_class = RankListSerializer


    # def list(self, request):
    #     queryset = UserProfile.objects.all().order_by('-passproblem')
    #     serializers = RankListSerializer(queryset, many=True)
    #     return Response(serializers.data)