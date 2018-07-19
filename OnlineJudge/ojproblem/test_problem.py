from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import *
from rest_framework.test import APIClient
import json


class OJProblemTestCase(TestCase):
    def setUp(self):
        # a predefined OJProblem
        p1 = OJProblem.objects.create(title='a-b', input1='2 2', output1='0', input2='2 3', output2='-1')
        OJProblem.objects.create(title='a-b', input1='2 2', output1='0', input2='2 3', output2='-1')
        OJProblem.objects.create(title='a-b3', input1='2 2', output1='0', input2='2 3', output2='-1')
        OJProblem.objects.create(title='a-b4', input1='2 2', output1='0', input2='2 3', output2='-1')
        OJProblem.objects.create(title='a-b5', input1='2 2', output1='0', input2='2 3', output2='-1')
        OJProblem.objects.create(title='a-b6', input1='2 2', output1='0', input2='2 3', output2='-1')
        OJProblem.objects.create(title='a-b', input1='2 2', output1='0', input2='2 3', output2='-1')
        OJProblem.objects.create(title='a-b', input1='2 2', output1='0', input2='2 3', output2='-1')
        OJProblem.objects.create(title='a-b', input1='2 2', output1='0', input2='2 3', output2='-1')
        OJProblem.objects.create(title='a-b', input1='2 2', output1='0', input2='2 3', output2='-1')
        OJProblem.objects.create(title='a-b', input1='2 2', output1='0', input2='2 3', output2='-1')
        OJProblem.objects.create(title='a-b', input1='2 2', output1='0', input2='2 3', output2='-1')
        OJProblem.objects.create(title='a-b', input1='2 2', output1='0', input2='2 3', output2='-1')
        OJProblem.objects.create(title='a-b', input1='2 2', output1='0', input2='2 3', output2='-1')
        OJProblem.objects.create(title='a-b', input1='2 2', output1='0', input2='2 3', output2='-1')
        # 15
        OJProblem.objects.create(title='a-b', input1='2 2', output1='0', input2='2 3', output2='-1')
        OJProblem.objects.create(title='a-b', input1='2 2', output1='0', input2='2 3', output2='-1')
        OJProblem.objects.create(title='a-b', input1='2 2', output1='0', input2='2 3', output2='-1')
        OJProblem.objects.create(title='a-b', input1='2 2', output1='0', input2='2 3', output2='-1')
        OJProblem.objects.create(title='a-b', input1='2 2', output1='0', input2='2 3', output2='-1')
        # 20
        OJProblem.objects.create(title='a-b', input1='2 2', output1='0', input2='2 3', output2='-1')
        OJProblem.objects.create(title='a-b', input1='2 2', output1='0', input2='2 3', output2='-1')
        OJProblem.objects.create(title='a-b', input1='2 2', output1='0', input2='2 3', output2='-1')

        u1 = User.objects.create_user(username='yigo', password='yigoyigo')
        
        OJUserAnswerAggr.objects.create(problem=p1, submitter=u1, result=1)
        self.client = APIClient()

    def test_get_problem_detail(self):
        res = self.client.get(reverse('problem_detail_api', args=['3']))
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content)
        self.assertEqual(js_dic['code'], 0)
        data = js_dic['data']
        self.assertEqual(data['title'], 'a-b3')

    def test_FET_get_not_existed_problem_detail(self):
        res = self.client.get(reverse('problem_detail_api', args=['333']))
        self.assertEqual(res.status_code, 404)

    def test_get_problem_list_without_auth(self):
        res = self.client.get(reverse('problem_list_api'))
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content)
        self.assertEqual(js_dic['count'], 23)
        results = js_dic['results']
        self.assertEqual(20, len(results))
        self.assertEqual(results[5]['title'], 'a-b6')

        exist = 'is_passed' in results[5]
        self.assertEqual(exist, False)

    def test_get_problem_list_with_auth(self):
        # login first
        self.client.login(username='yigo', password='yigoyigo')

        res = self.client.get(reverse('problem_list_api'))
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content)
        self.assertEqual(js_dic['count'], 23)
        results = js_dic['results']
        self.assertEqual(20, len(results))
        self.assertEqual(results[5]['title'], 'a-b6')

        exist = 'is_passed' in results[5]
        self.assertEqual(exist, True)
