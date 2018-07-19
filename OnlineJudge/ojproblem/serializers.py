from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from .models import *


class ShowProblemDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OJProblem
        fields = '__all__'


class ListProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OJProblem
        fields = ('id', 'title', 'pass_num', 'total_num',)


class ListAuthProblemSerializer(serializers.ModelSerializer):
    is_passed = serializers.SerializerMethodField('get_pass_status')

    def __init__(self, *args, **kwargs):
        self.user = kwargs['context']['request'].user
        super(ListAuthProblemSerializer, self).__init__(*args, **kwargs)

    def get_pass_status(self, obj):
        if OJUserAnswerAggr.objects.filter(problem=obj, submitter=self.user).exists():
            return 'pass'
        else:
            return 'N/A'

    class Meta:
        model = OJProblem
        fields = ('id', 'title', 'pass_num', 'total_num', 'is_passed')


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = OJAnswer
        exclude = ('raw_result',)