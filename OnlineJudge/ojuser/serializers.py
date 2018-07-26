from rest_framework import serializers
from django.contrib.auth.models import User
from .models import OJUserProfile
from django.core.exceptions import ObjectDoesNotExist


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(min_length=8, max_length=20)


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(min_length=8, max_length=20)
    activiation_code = serializers.CharField(max_length=20)


class UserProfileSerializer(serializers.ModelSerializer):
    signature = serializers.CharField(source='ojuserprofile.signature', allow_blank=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'signature')


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    signature = serializers.CharField(source='ojuserprofile.signature', allow_blank=True)

    class Meta:
        model = User
        fields = ('id', 'signature')

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('ojuserprofile', None)
        self.create_or_update_profile(instance, profile_data)
        return super(UserProfileUpdateSerializer, self).update(instance, validated_data)

    def create_or_update_profile(self, user, profile_data):
        profile, created = OJUserProfile.objects.get_or_create(user=user, defaults=profile_data)
        if not created and profile_data is not None:
            super(UserProfileUpdateSerializer, self).update(profile, profile_data)


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, max_length=20)


class UserRankSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = OJUserProfile
        fields = ('username', 'signature', 'pass_num', 'total_num',)