from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
import json

class AccountsTestCase(TestCase):
    def setUp(self):
        admin = User.objects.create_user(username='admin', password='yigo')
        admin.is_staff = True
        admin.save()
        normal = User.objects.create_user(username='testnormal', password='yigo')
        self.client = APIClient()

    def test_change_normal_user_password(self):
        # login with admin
        self.client.login(username='admin', password='yigo')
        # change testnormal's password
        res = self.client.post(reverse('admin_set_user_password_api', args=['2']), {'password' : '12345678'})
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['data'], 'Admin: Set password success.')
        # login with testnormal's old password
        res = self.client.post(reverse('user_login_api'), {'username': 'testnormal', 'password': 'yigo'})
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['code'], 1)
        self.assertEqual(js_dic['data'], 'Login failed.')
        # login with testnormal's new password
        res = self.client.post(reverse('user_login_api'), {'username': 'testnormal', 'password': '12345678'})
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['code'], 0)
        self.assertEqual(js_dic['data'], 'Login success.')

    def test_FET_change_normal_user_password_without_auth(self):
        # change testnormal's password
        res = self.client.post(reverse('admin_set_user_password_api', args=['2']), {'password' : '12345678'})
        self.assertEqual(res.status_code, 403)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['detail'], 'Authentication credentials were not provided.')

    def test_FET_change_normal_user_password_with_normal_user(self):
        # login with normal user
        self.client.login(username='testnormal', password='yigo')
        # change testnormal's password
        res = self.client.post(reverse('admin_set_user_password_api', args=['2']), {'password' : '12345678'})
        self.assertEqual(res.status_code, 403)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['detail'], 'You do not have permission to perform this action.')

    # test password limitation
    def test_FET_use_invalid_password_empty(self):
        # login with admin
        self.client.login(username='admin', password='yigo')
        # change testnormal's password
        res = self.client.post(reverse('admin_set_user_password_api', args=['2']), {'password' : ''})
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['data']['password'][0], 'This field may not be blank.')

    def test_FET_use_invalid_password_too_short(self):
        # login with admin
        self.client.login(username='admin', password='yigo')
        # change testnormal's password
        res = self.client.post(reverse('admin_set_user_password_api', args=['2']), {'password' : '1234'})
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['data']['password'][0], 'Ensure this field has at least 8 characters.')

    def test_FET_use_invalid_password_too_long(self):
        # login with admin
        self.client.login(username='admin', password='yigo')
        # change testnormal's password
        res = self.client.post(reverse('admin_set_user_password_api', args=['2']), {'password' : '1234565555555555555555555555555555555555555555555555555555555555555'})
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['data']['password'][0], 'Ensure this field has no more than 20 characters.')

    def test_update_normal_user_profile(self):
        # login with admin
        self.client.login(username='admin', password='yigo')    
        res = self.client.post(reverse('admin_edit_user_profile_api', args=['2']), {'description': 'sdssdfsdfsdfsddssfdsfdfsd搞一个大新闻dsd'})
        res = self.client.get(reverse('user_profile_api', args=['2']))
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['data']['description'], 'sdssdfsdfsdfsddssfdsfdfsd搞一个大新闻dsd')

    def test_FET_update_normal_user_profile_without_auth(self):
        # change profile 
        res = self.client.post(reverse('admin_edit_user_profile_api', args=['2']), {'description': 'sdssdfsdfsdfsddssfdsfdfsd搞一个大新闻dsd'})
        self.assertEqual(res.status_code, 403)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['detail'], 'Authentication credentials were not provided.')

    def test_FET_update_normal_user_profile_with_normal_user(self):
        # login with normal user
        self.client.login(username='testnormal', password='yigo')   
        # change profile 
        res = self.client.post(reverse('admin_edit_user_profile_api', args=['2']), {'description': 'sdssdfsdfsdfsddssfdsfdfsd搞一个大新闻dsd'})
        self.assertEqual(res.status_code, 403)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['detail'], 'You do not have permission to perform this action.')
