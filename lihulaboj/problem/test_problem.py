from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Problem
from rest_framework.test import APIClient
import json

from common import status


class AdminTestCase(TestCase):
    def setUp(self):
        admin = User.objects.create_user(username='admin', password='yigoyigo')
        admin.is_staff = True
        admin.save()
        # normal user
        User.objects.create_user(username='normal', password='boomshakalaka')
        self.client = APIClient()

    def test_create_a_new_problem(self):
        self.client.login(username='admin', password='yigoyigo')
        data = {
            'title' : 'a+b',
            'slug' : 'a_plus_b',
            'content' : 'add two numbers, output the result.',
            'max_cpu_time' : 133,
            'max_memory' : 199,
            'input1' : '1 2',
            'output1' : '3',
            'input2' : '2 9',
            'output2' : '11'
        }
        res = self.client.post(reverse('create_problem_api'), data)
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['data'], status.NEW_PROBLEM_SUCCESS)
        # Check in the DB
        problem_queryset = Problem.objects.filter(slug='a_plus_b')
        problem_len = len(problem_queryset)
        self.assertEqual(1, problem_len)
        # Check the content
        problem = problem_queryset.first()
        self.assertEqual(problem.title, 'a+b')
        self.assertEqual(problem.max_cpu_time, 133)
        self.assertEqual(problem.content, 'add two numbers, output the result.')
    
    def test_FET_create_a_new_problem_without_auth(self):
        data = {
            'title' : 'a+b',
            'slug' : 'a_plus_b',
            'content' : 'add two numbers, output the result.',
            'max_cpu_time' : 133,
            'max_memory' : 199,
            'input1' : '1 2',
            'output1' : '3',
            'input2' : '2 9',
            'output2' : '11'
        }
        res = self.client.post(reverse('create_problem_api'), data)
        self.assertEqual(res.status_code, 403)

    def test_FET_create_a_new_problem_without_admin(self):
        self.client.login(username='normal', password='boomshakalaka')
        data = {
            'title' : 'a+b',
            'slug' : 'a_plus_b',
            'content' : 'add two numbers, output the result.',
            'max_cpu_time' : 133,
            'max_memory' : 199,
            'input1' : '1 2',
            'output1' : '3',
            'input2' : '2 9',
            'output2' : '11'
        }
        res = self.client.post(reverse('create_problem_api'), data)
        self.assertEqual(res.status_code, 403)