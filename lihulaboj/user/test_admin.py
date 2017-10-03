from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
import json

from common import status


class AdminTestCase(TestCase):
    def setUp(self):
        admin = User.objects.create_user(username='admin', password='yigoyigo')
        admin.is_staff = True
        admin.save()
        normal = User.objects.create_user(username='testnormal', password='yigoyigo')
        admin2 = User.objects.create_user(username='admin2', password='yigoyigo')
        admin2.is_staff = True
        admin2.save()
        self.client = APIClient()

    def test_get_user_detail_by_id(self):
        self.client.login(username='admin', password='yigoyigo')
        # Get admin profile
        res = self.client.get(reverse('user_profile_by_id_api', args=['1']))
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['data']['username'], 'admin')
        # Get testnormal profile
        res = self.client.get(reverse('user_profile_by_id_api', args=['2']))
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['data']['username'], 'testnormal')

    def test_FET_get_user_detail_by_id_without_auth(self):
        # Get admin profile
        res = self.client.get(reverse('user_profile_by_id_api', args=['1']))
        self.assertEqual(res.status_code, 403)
        # Get testnormal profile
        res = self.client.get(reverse('user_profile_by_id_api', args=['2']))
        self.assertEqual(res.status_code, 403)

    def test_FET_get_user_detail_by_id_without_admin(self):
        self.client.login(username='testnormal', password='yigoyigo')
        # Get admin profile
        res = self.client.get(reverse('user_profile_by_id_api', args=['1']))
        self.assertEqual(res.status_code, 403)
        # Get testnormal profile
        res = self.client.get(reverse('user_profile_by_id_api', args=['2']))
        self.assertEqual(res.status_code, 403)

    def test_change_user_password_by_id(self):
        # Login as admin
        self.client.login(username='admin', password='yigoyigo')
        # Change testnormal's password
        res = self.client.post(reverse('change_password_by_id_api', args=['2']), {'password': '11111112'})
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['data'], status.ADMIN_UPDATE_PASSWORD_SUCCESS)
        # Check testnormal's password
        res = self.client.post(reverse('user_login_api'), {'username': 'testnormal', 'password': 'yigoyigo'}, format='json')
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['code'], 1)
        self.assertEqual(js_dic['data'], status.LOGIN_FAILED)
        # testnormal login with new password
        res = self.client.post(reverse('user_login_api'), {'username': 'testnormal', 'password': '11111112'}, format='json')
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['code'], 0)
        self.assertEqual(js_dic['data'], status.LOGIN_SUCCESS)

    def test_FET_change_user_password_by_id_too_long_password(self):
        # Login as admin
        self.client.login(username='admin', password='yigoyigo')
        # Change testnormal's password
        res = self.client.post(reverse('change_password_by_id_api', args=['2']), {'password': '123456789012345678901'})
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['data'], {'password' : ['Ensure this field has no more than 20 characters.']})

    def test_FET_change_user_password_by_id_without_admin(self):
        # Login as normal user
        self.client.login(username='testnormal', password='yigoyigo')
        # Change testnormal's password
        res = self.client.post(reverse('change_password_by_id_api', args=['2']), {'password': '11111112'})
        self.assertEqual(res.status_code, 403)

    def test_FET_change_user_password_by_id_without_auth(self):
        # Change testnormal's password
        res = self.client.post(reverse('change_password_by_id_api', args=['2']), {'password': '11111112'})
        self.assertEqual(res.status_code, 403)

    def test_FET_change_another_admin_password(self):
        # Login as admin
        self.client.login(username='admin', password='yigoyigo')
        # Change admin2's password
        res = self.client.post(reverse('change_password_by_id_api', args=['3']), {'admin2': '11111112'})
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['data'], status.UPDATE_ADMIN_PASSWORD_NOT_ALLOWED)
        # Try to login admin2 use old password
        res = self.client.post(reverse('user_login_api'), {'username': 'admin2', 'password': 'yigoyigo'}, format='json')
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['code'], 0)
        self.assertEqual(js_dic['data'], status.LOGIN_SUCCESS)        

    def test_update_user_profile_by_id(self):
        self.client.login(username='admin', password='yigoyigo')
        res = self.client.post(reverse('update_byid_api', args=['2']), {'signature': 'sdssdfsdfsdfsdfdsfdfsd搞一个大新闻dsd'})
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['data'], status.UPDATE_PROFILE_SUCCESS)
        
        # Get testnormal profile
        res = self.client.get(reverse('user_profile_by_id_api', args=['2']))
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['data']['signature'], 'sdssdfsdfsdfsdfdsfdfsd搞一个大新闻dsd')

    def test_FET_update_user_profile_by_id_without_auth(self):
        res = self.client.post(reverse('update_byid_api', args=['2']), {'signature': 'sdssdfsdfsdfsdfdsfdfsd搞一个大新闻dsd'})
        self.assertEqual(res.status_code, 403)

    def test_FET_update_user_profile_by_id_without_auth(self):
        self.client.login(username='testnormal', password='yigoyigo')
        res = self.client.post(reverse('update_byid_api', args=['2']), {'signature': 'sdssdfsdfsdfsdfdsfdfsd搞一个大新闻dsd'})
        self.assertEqual(res.status_code, 403)

    def test_FET_update_another_admin_profile_by_id(self):
        self.client.login(username='admin', password='yigoyigo')
        res = self.client.post(reverse('update_byid_api', args=['3']), {'signature' : 'sffds'})
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['data'], status.UPDATE_ADMIN_PROFILE_NOT_ALLOWED)

    def test_disable_normal_user(self):
        self.client.login(username='admin', password='yigoyigo')
        res = self.client.post(reverse('update_byid_api', args=['2']), {'is_active' : False})
        self.assertEqual(res.status_code, 200)
        self.client.logout()
        # Try to login with disabled user
        res = self.client.post(reverse('user_login_api'), {'username': 'testnormal', 'password': 'yigoyigo'}, format='json')
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['code'], 1)
        self.assertEqual(js_dic['data'], status.LOGIN_FAILED)