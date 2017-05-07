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

    # test password limitation
    def test_use_invalid_password(self):
        pass
