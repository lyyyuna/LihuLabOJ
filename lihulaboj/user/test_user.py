from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
import json

from common import status


class AccountsTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='yigo', password='yigo')
        User.objects.create_user(username='yigo2', password='yigo')
        User.objects.create_user(username='yigo3', password='pwchange')
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

    def test_get_self_profile(self):
        self.client.login(username='yigo2', password='yigo')
        res = self.client.get(reverse('user_myprofile_api'))
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['data']['username'], 'yigo2')

    def test_FET_get_self_profile_without_login(self):
        res = self.client.get(reverse('user_myprofile_api'))
        self.assertEqual(res.status_code, 403)

    def test_update_user_profile(self):
        self.client.login(username='yigo', password='yigo')
        res = self.client.post(reverse('edit_user_profile_api'), {'signature': 'sdssdfsdfsdfsdfdsfdfsd搞一个大新闻dsd'})
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['data'], status.UPDATE_PROFILE_SUCCESS)
        
        res = self.client.get(reverse('user_myprofile_api'))
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['data']['username'], 'yigo')
        self.assertEqual(js_dic['data']['signature'], 'sdssdfsdfsdfsdfdsfdfsd搞一个大新闻dsd')

    def test_FET_update_user_profile_without_auth(self):
        res = self.client.post(reverse('edit_user_profile_api'), {'signature': 'sdsd'})
        self.assertEqual(res.status_code, 403)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['detail'], 'Authentication credentials were not provided.')

    def test_update_user_password(self):
        self.client.login(username='yigo3', password='pwchange')
        res = self.client.post(reverse('change_user_password_api'), {'password': '11111111'})
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['data'], status.UPDATE_PASSWORD_SUCCESS)
        # logout, and login again with old password
        self.client.logout()
        self.client.login(username='yigo3', password='pwchange')
        res = self.client.get(reverse('user_myprofile_api'))
        self.assertEqual(res.status_code, 403)
        # logout, and login again with new password
        self.client.logout()
        self.client.login(username='yigo3', password='11111111')
        res = self.client.get(reverse('user_myprofile_api'))
        self.assertEqual(res.status_code, 200)

    def test_FET_update_user_password_without_auth(self):
        res = self.client.post(reverse('change_user_password_api'), {'password': '11111111'})
        self.assertEqual(res.status_code, 403)

    def test_FET_update_user_passwor_too_short(self):
        self.client.login(username='yigo3', password='pwchange')
        res = self.client.post(reverse('change_user_password_api'), {'password': '1234567'})
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['code'], 1)
        self.assertEqual(js_dic['data'], {'password' : ['Ensure this field has at least 8 characters.']})