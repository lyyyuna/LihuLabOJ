from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
import json

from common import status


class AccountsTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='yigo', password='yigo')
        self.client = APIClient()

    def test_user_login(self):
        res = self.client.post(reverse('user_login_api'), {'username': 'yigo', 'password': 'yigo'}, format='json')
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['code'], 0)
        self.assertEqual(js_dic['data'], status.LOGIN_SUCCESS)

    def test_FET_user_login_wrong_password(self):
        res = self.client.post(reverse('user_login_api'), {'username': 'yigo', 'password': 'yigo111'}, format='json')
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['code'], 1)
        self.assertEqual(js_dic['data'], status.LOGIN_FAILED)

    def test_FET_user_login_too_long_input(self):
        res = self.client.post(reverse('user_login_api'), {'username': 'yigo1111111111111111111111111111111111111111111111111111111112222222222222222222222222222222222222222222222223333333333333333333333333333333333333333333333333', 'password': 'yigo111'}, format='json')
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['code'], 1)
        self.assertEqual(js_dic['data'], status.INPUT_INVALID)

    def test_user_logout(self):
        res = self.client.post(reverse('user_login_api'), {'username': 'yigo', 'password': 'yigo'}, format='json')
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['code'], 0)
        self.assertEqual(js_dic['data'], status.LOGIN_SUCCESS)
        res = self.client.get(reverse('user_logout_api'))
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['code'], 0)
        self.assertEqual(js_dic['data'], status.LOGOUT_SUCCESS)

    def test_FET_user_logout_without_login(self):
        res = self.client.get(reverse('user_logout_api'))
        self.assertEqual(res.status_code, 403)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['detail'], 'Authentication credentials were not provided.')