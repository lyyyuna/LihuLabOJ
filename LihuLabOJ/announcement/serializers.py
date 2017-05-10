from rest_framework import serializers

from announcement.models import Announcement


class AnnouncementSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Announcement
        fields = ('id','url','owner', 'title', 'content', 'created','updated')

class AnnouncementTitleSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Announcement
        fields = ('url','owner', 'title')
