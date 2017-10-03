from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
import json

from .models import Invitation
from common import status


class AccountRegisterTest(TestCase):
    def setUp(self):
        User.objects.create_user(username='yigo', password='yigoyigo')
        Invitation.objects.create(code='abc123def')
        self.client = APIClient()

    def test_register_with_invitation_code(self):
        # register a new account
        res = self.client.post(reverse('user_register_api'), {'username': 'testnormal1', 'password': 'alotofyigo', 'invitation_code' : 'abc123def'})
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['code'], 0)
        self.assertEqual(js_dic['data'], status.REGISTER_SUCCESS)
        # try to login with the new account
        res = self.client.post(reverse('user_login_api'), {'username': 'testnormal1', 'password': 'alotofyigo'}, format='json')
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['code'], 0)
        self.assertEqual(js_dic['data'], status.LOGIN_SUCCESS)

    def test_FET_register_with_wrong_invitation_code(self):
        res = self.client.post(reverse('user_register_api'), {'username': 'testnormal1', 'password': 'alotofyigo', 'invitation_code' : 'wer'})
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['code'], 1)
        self.assertEqual(js_dic['data'], status.REGISTER_CODE_FAILED)

    def test_FET_register_with_too_short_password(self):
        res = self.client.post(reverse('user_register_api'), {'username': 'testnormal2', 'password': 'short', 'invitation_code' : 'abc123def'})
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['code'], 1)
        self.assertEqual(js_dic['data'], status.REGISTER_FAILED)