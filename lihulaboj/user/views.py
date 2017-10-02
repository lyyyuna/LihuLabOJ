from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import User, AnonymousUser

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.pagination import PageNumberPagination

from .serializers import UserLoginSerializer, UserProfileSerializer, PasswordSerializer, UserProfileAdminSerializer

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


class UserLogoutAPIView(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        auth.logout(request)
        return shortcuts.success_response(status.LOGOUT_SUCCESS)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    pagination_class = StandardResultsSetPagination
    serializer_class = UserProfileSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated,]
        elif self.action == 'update':
            self.permission_classes = [IsAuthenticated,]
        elif self.action == 'change_password':
            self.permission_classes = [IsAuthenticated,]
        elif self.action == 'retrieve_byid':
            self.permission_classes = [IsAdminUser,]
        elif self.action == 'change_password_byid':
            self.permission_classes = [IsAdminUser,]
        elif self.action == 'update_byid':
            self.permission_classes = [IsAdminUser,]
            pass
        return super(self.__class__, self).get_permissions()

    def retrieve(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return shortcuts.success_response(serializer.data)

    def update(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return shortcuts.success_response(status.UPDATE_PROFILE_SUCCESS)
        else:
            return shortcuts.error_response(status.UPDATE_PROFILE_FAILED)

    def change_password(self, request):
        user = request.user
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.data['password'])
            user.save()
            return shortcuts.success_response(status.UPDATE_PASSWORD_SUCCESS)
        else:
            return shortcuts.error_response(serializer.errors)

    def retrieve_byid(self, request, pk):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        profile = UserProfileAdminSerializer(user)
        return shortcuts.success_response(profile.data)    

    def change_password_byid(self, request, pk):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        # Cannot edit admin's password
        if user.is_staff == True:
            return shortcuts.error_response(status.UPDATE_ADMIN_PASSWORD_NOT_ALLOWED)

        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.data['password'])
            user.save()
            return shortcuts.success_response(status.ADMIN_UPDATE_PASSWORD_SUCCESS)
        else:
            return shortcuts.error_response(serializer.errors)

    def update_byid(self, request, pk):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        # Cannot edit admin's profile
        if user.is_staff == True:
            return shortcuts.error_response(status.UPDATE_ADMIN_PROFILE_NOT_ALLOWED)
        
        serializer = UserProfileAdminSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return shortcuts.success_response(status.UPDATE_PROFILE_SUCCESS)
        else:
            return shortcuts.error_response(status.UPDATE_PROFILE_FAILED)