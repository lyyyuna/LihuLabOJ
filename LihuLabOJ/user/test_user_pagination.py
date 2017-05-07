from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
import json

class UserPaginationTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='yigo1', password='yigo')
        User.objects.create_user(username='yigo2', password='yigo')
        User.objects.create_user(username='yigo3', password='yigo')
        User.objects.create_user(username='yigo4', password='yigo')
        User.objects.create_user(username='yigo5', password='yigo')
        User.objects.create_user(username='yigo6', password='yigo')
        User.objects.create_user(username='yigo7', password='yigo')
        User.objects.create_user(username='yigo8', password='yigo')
        User.objects.create_user(username='yigo9', password='yigo')
        User.objects.create_user(username='yigo10', password='yigo')
        User.objects.create_user(username='yigo11', password='yigo')                
        User.objects.create_user(username='yigo12', password='yigo')        
        User.objects.create_user(username='yigo13', password='yigo')
        User.objects.create_user(username='yigo14', password='yigo')
        User.objects.create_user(username='yigo15', password='yigo')
        User.objects.create_user(username='yigo16', password='yigo')
        User.objects.create_user(username='yigo17', password='yigo')
        User.objects.create_user(username='yigo18', password='yigo')
        User.objects.create_user(username='yigo19', password='yigo')
        User.objects.create_user(username='yigo20', password='yigo')
        User.objects.create_user(username='yigo21', password='yigo')
        User.objects.create_user(username='yigo22', password='yigo')
        User.objects.create_user(username='yigo23', password='yigo')                                                                                
        self.client = APIClient()

    def test_list_1st_page_users(self):
        res = self.client.get(reverse('user_allprofile_api'))
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['count'], 23)
        self.assertEqual(js_dic['next'], 'http://testserver/user/allprofile?page=2')
        self.assertEqual(js_dic['previous'], None)

