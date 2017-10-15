from rest_framework import serializers
from .models import Answser, Problem


class EditProblemSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return Problem.objects.create(**validated_data)

    class Meta:
        model = Problem
        exclude = ('create_time',)


class ShowProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'


class AnswserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Answser
        fields = '__all__'