from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
import json

class AdminTestCase(TestCase):
    def setUp(self):
        admin = User.objects.create_user(username='admin', password='yigo')
        admin.is_staff = True
        admin.save()
        normal = User.objects.create_user(username='testnormal', password='yigo')
        self.client = APIClient()

    def test_get_user_detail_by_id(self):
        res = self.client.get(reverse('user_profile_by_id_api', args=['1']))
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        print (js_dic)