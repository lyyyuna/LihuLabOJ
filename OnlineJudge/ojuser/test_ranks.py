from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
import json

from .models import *


class UserRanksTest(TestCase):
    def setUp(self):
        u1 = User.objects.create_user(username='yigo1', password='yigoyigo')
        u2 = User.objects.create_user(username='yigo2', password='yigoyigo')
        u3 = User.objects.create_user(username='yigo3', password='yigoyigo')
        u4 = User.objects.create_user(username='yigo4', password='yigoyigo')
        u5 = User.objects.create_user(username='yigo5', password='yigoyigo')
        # 5
        u6 = User.objects.create_user(username='yigo6', password='yigoyigo')
        u7 = User.objects.create_user(username='yigo7', password='yigoyigo')
        u8 = User.objects.create_user(username='yigo8', password='yigoyigo')
        u9 = User.objects.create_user(username='yigo9', password='yigoyigo')
        u10 = User.objects.create_user(username='yigo10', password='yigoyigo')
        # 10
        u11 = User.objects.create_user(username='yigo11', password='yigoyigo')
        u12 = User.objects.create_user(username='yigo12', password='yigoyigo')
        u13 = User.objects.create_user(username='yigo13', password='yigoyigo')
        u14 = User.objects.create_user(username='yigo14', password='yigoyigo')
        u15 = User.objects.create_user(username='yigo15', password='yigoyigo')
        # 15
        u16 = User.objects.create_user(username='yigo16', password='yigoyigo')
        u17 = User.objects.create_user(username='yigo17', password='yigoyigo')
        u18 = User.objects.create_user(username='yigo18', password='yigoyigo')
        u19 = User.objects.create_user(username='yigo19', password='yigoyigo')
        u20 = User.objects.create_user(username='yigo20', password='yigoyigo')
        # 20
        u21 = User.objects.create_user(username='yigo21', password='yigoyigo')


        OJUserProfile.objects.create(user=u1, pass_num=1, total_num=1)
        OJUserProfile.objects.create(user=u2, pass_num=2, total_num=2)
        OJUserProfile.objects.create(user=u3, pass_num=3, total_num=3)
        OJUserProfile.objects.create(user=u4, pass_num=4, total_num=4)
        OJUserProfile.objects.create(user=u5, pass_num=5, total_num=10)
        # 5
        OJUserProfile.objects.create(user=u6, pass_num=5, total_num=9)
        OJUserProfile.objects.create(user=u7, pass_num=1, total_num=1)
        OJUserProfile.objects.create(user=u8, pass_num=2, total_num=2)
        OJUserProfile.objects.create(user=u9, pass_num=3, total_num=3)
        OJUserProfile.objects.create(user=u10, pass_num=4, total_num=4)
        # 10
        OJUserProfile.objects.create(user=u11, pass_num=3, total_num=9)
        OJUserProfile.objects.create(user=u12, pass_num=1, total_num=1)
        OJUserProfile.objects.create(user=u13, pass_num=2, total_num=2)
        OJUserProfile.objects.create(user=u14, pass_num=3, total_num=3)
        OJUserProfile.objects.create(user=u15, pass_num=4, total_num=4)
        # 15
        OJUserProfile.objects.create(user=u16, pass_num=3, total_num=9)
        OJUserProfile.objects.create(user=u17, pass_num=1, total_num=1)
        OJUserProfile.objects.create(user=u18, pass_num=2, total_num=2)
        OJUserProfile.objects.create(user=u19, pass_num=3, total_num=3)
        OJUserProfile.objects.create(user=u20, pass_num=4, total_num=4)
        # 20
        OJUserProfile.objects.create(user=u21, pass_num=4, total_num=4)

        self.client = APIClient()

    def test_get_user_ranks(self):
        res = self.client.get(reverse('user_rank_list_api'))
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content)

        self.assertEqual(js_dic['count'], 21)
        results = js_dic['results']
        self.assertEqual(20, len(results))        
        self.assertEqual(results[0]['username'], 'yigo6')