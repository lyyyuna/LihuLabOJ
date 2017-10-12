from rest_framework import serializers
from .models import Answser


class AnswserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Answser
        fields = '__all__'