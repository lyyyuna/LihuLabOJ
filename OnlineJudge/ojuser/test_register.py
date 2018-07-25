from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
import json

from .models import *


class AccountRegisterTest(TestCase):
    def setUp(self):
        User.objects.create_user(username='yigo', password='yigoyigo')
        ActiviationCode.objects.create(key='abc123def')
        self.client = APIClient()

    def test_register_with_activiation_code(self):
        # register a new account
        res = self.client.post(reverse('user_register_api'),
                            {'username' : 'testnormal1', 
                             'password' : 'yur$$24.',
                             'activiation_code' : 'abc123def'})
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content)
        self.assertEqual(js_dic['code'], 0)
        self.assertEqual(js_dic['data'], 'register success')

        # login with the new account
        res = self.client.post(reverse('user_login_api'),
                            {
                                'username' : 'testnormal1', 
                                'password' : 'yur$$24.',
                            })
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content)
        self.assertEqual(js_dic['code'], 0)
        self.assertEqual(js_dic['data'], 'login success')

        # should also create user's profile model
        res = self.client.get(reverse('user_myprofile_api'))
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content)
        self.assertEqual(js_dic['data']['username'], 'testnormal1')

    def test_FET_register_with_wrong_activiation_code(self):
        res = self.client.post(reverse('user_register_api'),
                            {'username' : 'testnormal1', 
                             'password' : 'yur$$24.',
                             'activiation_code' : 'wrongwrong'})
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content)
        self.assertEqual(js_dic['code'], 1)
        self.assertEqual(js_dic['data'], 'wrong ac key')

    def test_FET_register_with_too_short_password(self):
        res = self.client.post(reverse('user_register_api'),
                            {'username' : 'testnormal1', 
                             'password' : 'yur',
                             'activiation_code' : 'abc123def'})
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content)
        self.assertEqual(js_dic['code'], 1)
        self.assertEqual(js_dic['data'], 'input invalid')

    def test_FET_register_with_existed_username(self):
        # register a new account
        res = self.client.post(reverse('user_register_api'),
                            {'username' : 'testnormal1', 
                             'password' : 'yur$$24.',
                             'activiation_code' : 'abc123def'})
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content)
        self.assertEqual(js_dic['code'], 0)
        self.assertEqual(js_dic['data'], 'register success')

        # register existed account
        res = self.client.post(reverse('user_register_api'),
                            {'username' : 'testnormal1', 
                             'password' : 'yur$$24.',
                             'activiation_code' : 'abc123def'})
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content)
        self.assertEqual(js_dic['code'], 1)
        self.assertEqual(js_dic['data'], 'username already exists')