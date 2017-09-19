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