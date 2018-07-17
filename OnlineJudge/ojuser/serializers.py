from rest_framework import serializers
from django.contrib.auth.models import User
from .models import OJUserProfile


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(min_length=8, max_length=20)


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(min_length=8, max_length=20)
    activiation_code = serializers.CharField(max_length=20)