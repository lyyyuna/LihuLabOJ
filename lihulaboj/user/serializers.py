from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=30)