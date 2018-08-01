from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import *
from rest_framework.test import APIClient
import json


class OJAnswerTestCase(TestCase):
    def setUp(self):
        u1 = User.objects.create_user(username='yigo', password='yigoyigo')
        p1 = OJProblem.objects.create(title='a-b', input1='2 2', output1='0', input2='2 3', output2='-1')

        OJAnswer.objects.create(problem=p1, submitter=u1, status='pending', source_code='print "hello, world"', result=-1, raw_result='sdfsdf', cpu=111, memory=112)
        OJAnswer.objects.create(problem=p1, submitter=u1, status='pending', source_code='print "hello, world"', result=-1, raw_result='sdfsdf', cpu=111, memory=112)
        OJAnswer.objects.create(problem=p1, submitter=u1, status='pending', source_code='print "hello, world"', result=-1, raw_result='sdfsdf', cpu=111, memory=112)
        OJAnswer.objects.create(problem=p1, submitter=u1, status='pending', source_code='print "hello, world"', result=-1, raw_result='sdfsdf', cpu=111, memory=112)
        OJAnswer.objects.create(problem=p1, submitter=u1, status='pending', source_code='print "hello, world"', result=-1, raw_result='sdfsdf', cpu=111, memory=112)

        OJAnswer.objects.create(problem=p1, submitter=u1, status='pending', source_code='print "hello, world"', result=-1, raw_result='sdfsdf', cpu=111, memory=112)
        OJAnswer.objects.create(problem=p1, submitter=u1, status='pending', source_code='print "hello, world"', result=-1, raw_result='sdfsdf', cpu=111, memory=112)
        OJAnswer.objects.create(problem=p1, submitter=u1, status='pending', source_code='print "hello, world"', result=-1, raw_result='sdfsdf', cpu=111, memory=112)
        OJAnswer.objects.create(problem=p1, submitter=u1, status='pending', source_code='print "hello, world"', result=-1, raw_result='sdfsdf', cpu=111, memory=112)
        OJAnswer.objects.create(problem=p1, submitter=u1, status='pending', source_code='print "hello, world"', result=-1, raw_result='sdfsdf', cpu=111, memory=112)
        # 10
        OJAnswer.objects.create(problem=p1, submitter=u1, status='pending', source_code='print "hello, world"', result=-1, raw_result='sdfsdf', cpu=111, memory=112)
        OJAnswer.objects.create(problem=p1, submitter=u1, status='pending', source_code='print "hello, world"', result=-1, raw_result='sdfsdf', cpu=111, memory=112)
        OJAnswer.objects.create(problem=p1, submitter=u1, status='pending', source_code='print "hello, world"', result=-1, raw_result='sdfsdf', cpu=111, memory=112)
        OJAnswer.objects.create(problem=p1, submitter=u1, status='pending', source_code='print "hello, world"', result=-1, raw_result='sdfsdf', cpu=111, memory=112)
        OJAnswer.objects.create(problem=p1, submitter=u1, status='pending', source_code='print "hello, world"', result=-1, raw_result='sdfsdf', cpu=111, memory=112)

        OJAnswer.objects.create(problem=p1, submitter=u1, status='pending', source_code='print "hello, world"', result=-1, raw_result='sdfsdf', cpu=111, memory=112)
        OJAnswer.objects.create(problem=p1, submitter=u1, status='pending', source_code='print "hello, world"', result=-1, raw_result='sdfsdf', cpu=111, memory=112)
        OJAnswer.objects.create(problem=p1, submitter=u1, status='pending', source_code='print "hello, world"', result=-1, raw_result='sdfsdf', cpu=111, memory=112)
        OJAnswer.objects.create(problem=p1, submitter=u1, status='pending', source_code='print "hello, world"', result=-1, raw_result='sdfsdf', cpu=111, memory=112)
        OJAnswer.objects.create(problem=p1, submitter=u1, status='pending', source_code='print "hello, world"', result=-1, raw_result='sdfsdf', cpu=111, memory=112)
        # 20
        OJAnswer.objects.create(problem=p1, submitter=u1, status='pending', source_code='print "hello, world"', result=-1, raw_result='sdfsdf', cpu=116, memory=112)
        OJAnswer.objects.create(problem=p1, submitter=u1, status='pending', source_code='print "hello, world"', result=-1, raw_result='sdfsdf', cpu=111, memory=112)
        OJAnswer.objects.create(problem=p1, submitter=u1, status='pending', source_code='print "hello, world"', result=-1, raw_result='sdfsdf', cpu=111, memory=112)
        OJAnswer.objects.create(problem=p1, submitter=u1, status='pending', source_code='print "hello, world"', result=-1, raw_result='sdfsdf', cpu=111, memory=112)
        OJAnswer.objects.create(problem=p1, submitter=u1, status='pending', source_code='print "hello, world"', result=-1, raw_result='sdfsdf', cpu=111, memory=112)
        self.client = APIClient()

    def test_view_detail_answer_with_auth(self):
        self.client.login(username='yigo', password='yigoyigo')
        res = self.client.get(reverse('answer_detail_api', args=['1']))
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content)
        self.assertEqual(js_dic['data']['source_code'], 'print "hello, world"')
        self.assertEqual(js_dic['data']['cpu'], 111)

    def test_FET_view_detail_answer_withoutauth(self):
        res = self.client.get(reverse('answer_detail_api', args=['1']))
        self.assertEqual(res.status_code, 403)

    def test_get_myanswer_list_for_one_problem_with_auth(self):
        self.client.login(username='yigo', password='yigoyigo')
        res = self.client.get(reverse('problem_myanswer_list_api', args=['1']))
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content)

        self.assertEqual(js_dic['count'], 25)
        results = js_dic['results']
        self.assertEqual(20, len(results))        
        self.assertEqual(results[4]['cpu'], 116) # order by desc

    def test_get_myanswer_list_for_one_problem_without_auth(self):
        res = self.client.get(reverse('problem_myanswer_list_api', args=['1']))
        self.assertEqual(res.status_code, 403)

    def test_get_myanswer_list_with_auth(self):
        self.client.login(username='yigo', password='yigoyigo')
        res = self.client.get(reverse('myanswer_list_api'))
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content)

        self.assertEqual(js_dic['count'], 25)
        results = js_dic['results']
        self.assertEqual(20, len(results))        
        self.assertEqual(results[4]['cpu'], 116) # order by desc

    def test_get_myanswer_list_without_auth(self):
        res = self.client.get(reverse('myanswer_list_api'))
        self.assertEqual(res.status_code, 403)