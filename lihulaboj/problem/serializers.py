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


class ListProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ('id', 'title', 'pass_num', 'total_num',)


class AnswserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answser
        fields = '__all__'


class SubmitAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answser
        fields = ('source_code', 'language',)