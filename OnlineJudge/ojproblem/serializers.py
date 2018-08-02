from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from .models import *


class ShowProblemDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OJProblem
        exclude = ('input2', 'output2',)


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
            uaggr = OJUserAnswerAggr.objects.get(problem=obj, submitter=self.user)
            if uaggr.result == 0:
                return 'pass'
            else:
                return 'failed' 
        else:
            return 'N/A'

    class Meta:
        model = OJProblem
        fields = ('id', 'title', 'pass_num', 'total_num', 'is_passed')


class AnswerSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = OJAnswer
        exclude = ('raw_result',)


class AnswerBriefSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = OJAnswer
        fields = ('id', 'create_time', 'problem', 'result', 'cpu')


class AnswerRankSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='submitter.username')

    class Meta:
        model = OJUserAnswerAggr
        fields = ('id', 'username', 'problem', 'answer', 'cpu', 'memory')


class SubmitAnswerSerializer(serializers.ModelSerializer):
    source_code = serializers.CharField(max_length=2048)

    class Meta:
        model = OJAnswer
        fields = ('source_code',)