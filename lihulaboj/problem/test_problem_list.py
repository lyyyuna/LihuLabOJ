from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Problem
from rest_framework.test import APIClient
import json

from common import status


class ProblemListTestCase(TestCase):
    def setUp(self):
        # a predefined problem
        Problem.objects.create(title='a-b', slug='a_minus_b1', max_cpu_time=133, max_memory=199, input1='2 2', output1='0', input2='2 3', output2='-1')
        Problem.objects.create(title='a-b', slug='a_minus_b2', max_cpu_time=133, max_memory=199, input1='2 2', output1='0', input2='2 3', output2='-1')
        Problem.objects.create(title='a-b3', slug='a_minus_b3', max_cpu_time=133, max_memory=199, input1='2 2', output1='0', input2='2 3', output2='-1')
        Problem.objects.create(title='a-b4', slug='a_minus_b4', max_cpu_time=133, max_memory=199, input1='2 2', output1='0', input2='2 3', output2='-1')
        Problem.objects.create(title='a-b5', slug='a_minus_b5', max_cpu_time=133, max_memory=199, input1='2 2', output1='0', input2='2 3', output2='-1')
        Problem.objects.create(title='a-b6', slug='a_minus_b6', max_cpu_time=133, max_memory=199, input1='2 2', output1='0', input2='2 3', output2='-1')
        Problem.objects.create(title='a-b', slug='a_minus_b7', max_cpu_time=133, max_memory=199, input1='2 2', output1='0', input2='2 3', output2='-1')
        Problem.objects.create(title='a-b', slug='a_minus_b8', max_cpu_time=133, max_memory=199, input1='2 2', output1='0', input2='2 3', output2='-1')
        Problem.objects.create(title='a-b', slug='a_minus_b9', max_cpu_time=133, max_memory=199, input1='2 2', output1='0', input2='2 3', output2='-1')
        Problem.objects.create(title='a-b', slug='a_minus_b10', max_cpu_time=133, max_memory=199, input1='2 2', output1='0', input2='2 3', output2='-1')
        Problem.objects.create(title='a-b', slug='a_minus_b11', max_cpu_time=133, max_memory=199, input1='2 2', output1='0', input2='2 3', output2='-1')
        Problem.objects.create(title='a-b', slug='a_minus_b12', max_cpu_time=133, max_memory=199, input1='2 2', output1='0', input2='2 3', output2='-1')
        Problem.objects.create(title='a-b', slug='a_minus_b13', max_cpu_time=133, max_memory=199, input1='2 2', output1='0', input2='2 3', output2='-1')
        Problem.objects.create(title='a-b', slug='a_minus_b14', max_cpu_time=133, max_memory=199, input1='2 2', output1='0', input2='2 3', output2='-1')
        Problem.objects.create(title='a-b', slug='a_minus_b15', max_cpu_time=133, max_memory=199, input1='2 2', output1='0', input2='2 3', output2='-1')

        Problem.objects.create(title='a-b', slug='a_minus_b16', max_cpu_time=133, max_memory=199, input1='2 2', output1='0', input2='2 3', output2='-1')
        Problem.objects.create(title='a-b', slug='a_minus_b17', max_cpu_time=133, max_memory=199, input1='2 2', output1='0', input2='2 3', output2='-1')
        Problem.objects.create(title='a-b', slug='a_minus_b18', max_cpu_time=133, max_memory=199, input1='2 2', output1='0', input2='2 3', output2='-1')
        Problem.objects.create(title='a-b', slug='a_minus_b19', max_cpu_time=133, max_memory=199, input1='2 2', output1='0', input2='2 3', output2='-1')

        self.client = APIClient()

    def test_get_problem_list(self):
        res = self.client.get(reverse('problem_list_api'))
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['count'], 19)
        results = js_dic['results']
        self.assertEqual(15, len(results))
        self.assertEqual(results[5]['title'], 'a-b6')

    def test_get_problem_detail(self):
        res = self.client.get(reverse('problem_detail_api', args=['3']))
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['code'], 0)
        data = js_dic['data']
        self.assertEqual(data['title'], 'a-b3')