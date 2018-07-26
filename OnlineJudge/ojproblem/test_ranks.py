from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import *
from rest_framework.test import APIClient
import json


class OJProblemRanksTestCase(TestCase):
    def setUp(self):
        p1 = OJProblem.objects.create(title='a-b', input1='2 2', output1='0', input2='2 3', output2='-1')

        u1 = User.objects.create_user(username='yigo1', password='yigoyigo')
        u2 = User.objects.create_user(username='yigo2', password='yigoyigo')

        a1 = OJAnswer.objects.create(problem=p1, submitter=u1, status='pending', source_code='print "hello, world"', result=-1, raw_result='sdfsdf', cpu=111, memory=112)

        OJUserAnswerAggr.objects.create(problem=p1, submitter=u1, answer=a1, result=0, cpu=22, memory=22)
        OJUserAnswerAggr.objects.create(problem=p1, submitter=u2, answer=a1, result=0, cpu=21, memory=22)
        OJUserAnswerAggr.objects.create(problem=p1, submitter=u1, answer=a1, result=0, cpu=20, memory=22)
        OJUserAnswerAggr.objects.create(problem=p1, submitter=u1, answer=a1, result=0, cpu=22, memory=22)
        OJUserAnswerAggr.objects.create(problem=p1, submitter=u1, answer=a1, result=0, cpu=22, memory=22)
        # 5
        OJUserAnswerAggr.objects.create(problem=p1, submitter=u1, answer=a1, result=0, cpu=22, memory=22)
        OJUserAnswerAggr.objects.create(problem=p1, submitter=u1, answer=a1, result=0, cpu=22, memory=22)
        OJUserAnswerAggr.objects.create(problem=p1, submitter=u2, answer=a1, result=0, cpu=22, memory=22)
        OJUserAnswerAggr.objects.create(problem=p1, submitter=u1, answer=a1, result=0, cpu=22, memory=22)
        OJUserAnswerAggr.objects.create(problem=p1, submitter=u1, answer=a1, result=0, cpu=22, memory=22)
        # 10
        OJUserAnswerAggr.objects.create(problem=p1, submitter=u1, answer=a1, result=0, cpu=22, memory=22)
        OJUserAnswerAggr.objects.create(problem=p1, submitter=u1, answer=a1, result=0, cpu=22, memory=22)
        OJUserAnswerAggr.objects.create(problem=p1, submitter=u2, answer=a1, result=0, cpu=22, memory=22)
        OJUserAnswerAggr.objects.create(problem=p1, submitter=u1, answer=a1, result=0, cpu=22, memory=22)
        OJUserAnswerAggr.objects.create(problem=p1, submitter=u1, answer=a1, result=0, cpu=22, memory=22)
        # 15
        OJUserAnswerAggr.objects.create(problem=p1, submitter=u1, answer=a1, result=0, cpu=22, memory=22)
        OJUserAnswerAggr.objects.create(problem=p1, submitter=u2, answer=a1, result=0, cpu=22, memory=22)
        OJUserAnswerAggr.objects.create(problem=p1, submitter=u1, answer=a1, result=0, cpu=22, memory=22)
        OJUserAnswerAggr.objects.create(problem=p1, submitter=u1, answer=a1, result=0, cpu=13, memory=22)
        OJUserAnswerAggr.objects.create(problem=p1, submitter=u2, answer=a1, result=0, cpu=10, memory=21)
        # 20
        OJUserAnswerAggr.objects.create(problem=p1, submitter=u2, answer=a1, result=1, cpu=10, memory=22)
        OJUserAnswerAggr.objects.create(problem=p1, submitter=u1, answer=a1, result=0, cpu=10, memory=22)

        self.client = APIClient()

    def test_get_problem_answer_ranks(self):
        res = self.client.get(reverse('problem_rank_list_api', args=['1']))
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content)
        self.assertEqual(js_dic['count'], 21)
        results = js_dic['results']
        self.assertEqual(20, len(results))
        self.assertEqual(results[0]['id'], 20)