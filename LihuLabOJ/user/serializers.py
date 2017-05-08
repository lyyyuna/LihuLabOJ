from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=30)


class UserProfileSerializer(serializers.ModelSerializer):
    signature = serializers.CharField(source='userprofile.signature', allow_blank=True)
    description = serializers.CharField(source='userprofile.description', allow_blank=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'signature', 'description')

    # def create(self, validated_data):
    #     profile_data = validated_data.pop('userprofile', None)
    #     user = super(UserProfileSerializer, self).create(validated_data)
    #     self.create_or_update_profile(user, profile_data)
    #     return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('userprofile', None)
        self.create_or_update_profile(instance, profile_data)
        return super(UserProfileSerializer, self).update(instance, validated_data)

    def create_or_update_profile(self, user, profile_data):
        profile, created = UserProfile.objects.get_or_create(user=user, defaults=profile_data)
        if not created and profile_data is not None:
            super(UserProfileSerializer, self).update(profile, profile_data)


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, max_length=20)


class AdminUserProfileSerializer(serializers.ModelSerializer):
    signature = serializers.CharField(source='userprofile.signature', allow_blank=True)
    description = serializers.CharField(source='userprofile.description', allow_blank=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'signature', 'description', 'is_staff', 'is_active')

    # def create(self, validated_data):
    #     profile_data = validated_data.pop('userprofile', None)
    #     user = super(UserProfileSerializer, self).create(validated_data)
    #     self.create_or_update_profile(user, profile_data)
    #     return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('userprofile', None)
        self.create_or_update_profile(instance, profile_data)
        return super(AdminUserProfileSerializer, self).update(instance, validated_data)

    def create_or_update_profile(self, user, profile_data):
        profile, created = UserProfile.objects.get_or_create(user=user, defaults=profile_data)
        if not created and profile_data is not None:
            super(AdminUserProfileSerializer, self).update(profile, profile_data)


class RankListSerializer(serializers.ModelSerializer):
    userid = serializers.IntegerField(source='user.id')
    username = serializers.CharField(source='user.username')

    class Meta:
        model = UserProfile
        fields = ('userid', 'username', 'passproblem', 'failedproblem', 'signature')