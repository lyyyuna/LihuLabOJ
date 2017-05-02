from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
import json

class AccountsTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='yigo', password='yigo')
        self.client = APIClient()

    def test_user_login(self):
        res = self.client.post(reverse('user_login_api'), {'username': 'yigo', 'password': 'yigo'}, format='json')
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content)
        self.assertEqual(js_dic['code'], 0)
        self.assertEqual(js_dic['data'], 'Login success.')

    def test_FET_user_logout_without_login(self):
        res = self.client.get(reverse('user_logout_api'))
        self.assertEqual(res.status_code, 403)
        js_dic = json.loads(res.content)
        self.assertEqual(js_dic['detail'], 'Authentication credentials were not provided.')

    def test_user_logout(self):
        res = self.client.post(reverse('user_login_api'), {'username': 'yigo', 'password': 'yigo'}, format='json')
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content)
        self.assertEqual(js_dic['code'], 0)
        self.assertEqual(js_dic['data'], 'Login success.')
        res = self.client.get(reverse('user_logout_api'))
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content)
        self.assertEqual(js_dic['code'], 0)
        self.assertEqual(js_dic['data'], 'Logout success.')