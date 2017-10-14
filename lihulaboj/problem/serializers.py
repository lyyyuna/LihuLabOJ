from rest_framework import serializers
from .models import Answser, Problem


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        


class AnswserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Answser
        fields = '__all__'