from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
import json
from .models import UserProfile

class RankListTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(username='yigo1', password='yigo')
        user2 = User.objects.create_user(username='yigo2', password='yigo')
        user3 = User.objects.create_user(username='yigo3', password='yigo')
        user4 = User.objects.create_user(username='yigo4', password='yigo')
        user5 = User.objects.create_user(username='yigo5', password='yigo')
        user6 = User.objects.create_user(username='yigo6', password='yigo')
        user7 = User.objects.create_user(username='yigo7', password='yigo')
        user8 = User.objects.create_user(username='yigo8', password='yigo')
        user9 = User.objects.create_user(username='yigo9', password='yigo')
        user10 = User.objects.create_user(username='yigo10', password='yigo')
        user11 = User.objects.create_user(username='yigo11', password='yigo')
        user12 = User.objects.create_user(username='yigo12', password='yigo')
        user13 = User.objects.create_user(username='yigo13', password='yigo')
        user14 = User.objects.create_user(username='yigo14', password='yigo')
        user15 = User.objects.create_user(username='yigo15', password='yigo')
        user16 = User.objects.create_user(username='yigo16', password='yigo')
        user17 = User.objects.create_user(username='yigo17', password='yigo')
        user18 = User.objects.create_user(username='yigo18', password='yigo')
        user19 = User.objects.create_user(username='yigo19', password='yigo')
        user20 = User.objects.create_user(username='yigo20', password='yigo')
        user21 = User.objects.create_user(username='yigo21', password='yigo')
        user22 = User.objects.create_user(username='yigo22', password='yigo')
        user23 = User.objects.create_user(username='yigo23', password='yigo')
        user24 = User.objects.create_user(username='yigo24', password='yigo')

        UserProfile.objects.get_or_create(user=user1, signature='sdsdsd', passproblem=1, failedproblem=10)
        UserProfile.objects.get_or_create(user=user2, signature='搞个大学问', passproblem=10)
        UserProfile.objects.get_or_create(user=user3, signature='搞个小新闻', passproblem=5)
        UserProfile.objects.get_or_create(user=user4, signature='run fast', passproblem=43)
        UserProfile.objects.get_or_create(user=user5, signature='sdsdsd', passproblem=11)
        UserProfile.objects.get_or_create(user=user6, signature='搞个大学问', passproblem=10)
        UserProfile.objects.get_or_create(user=user7, signature='搞个小新闻', passproblem=15)
        UserProfile.objects.get_or_create(user=user8, signature='run fast', passproblem=43)
        UserProfile.objects.get_or_create(user=user9, signature='sdsdsd', passproblem=13)
        UserProfile.objects.get_or_create(user=user10, signature='搞个大学问', passproblem=110, failedproblem=101)
        UserProfile.objects.get_or_create(user=user11, signature='搞个小新闻', passproblem=52)
        UserProfile.objects.get_or_create(user=user12, signature='run fast', passproblem=43)
        UserProfile.objects.get_or_create(user=user13, signature='sdsdsd', passproblem=16)
        UserProfile.objects.get_or_create(user=user14, signature='搞个大学问', passproblem=20)
        UserProfile.objects.get_or_create(user=user15, signature='搞个小新闻', passproblem=25)
        UserProfile.objects.get_or_create(user=user16, signature='run fast', passproblem=23)
        UserProfile.objects.get_or_create(user=user17, signature='sdsdsd', passproblem=1)
        UserProfile.objects.get_or_create(user=user18, signature='搞个大学问', passproblem=10)
        UserProfile.objects.get_or_create(user=user19, signature='搞个小新闻', passproblem=5)
        UserProfile.objects.get_or_create(user=user20, signature='run fast', passproblem=43)
        UserProfile.objects.get_or_create(user=user21, signature='sdsdsd', passproblem=110, failedproblem=12)
        UserProfile.objects.get_or_create(user=user22, signature='搞个大学问', passproblem=10)
        UserProfile.objects.get_or_create(user=user23, signature='搞个小新闻', passproblem=5)
        UserProfile.objects.get_or_create(user=user24, signature='run fast', passproblem=43)


    def test_get_ranklist(self):
        res = self.client.get(reverse('get_ranklist_api'))
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['count'], 24)
        self.assertEqual(js_dic['next'], 'http://testserver/user/rank?page=2')
        self.assertEqual(js_dic['previous'], None)
        self.assertEqual(js_dic['results'][0]['userid'], 21)
        self.assertEqual(js_dic['results'][1]['userid'], 10)