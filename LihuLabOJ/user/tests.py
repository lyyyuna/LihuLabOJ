from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient

class AccountsTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='yigo', password='yigo')
        self.client = APIClient()

    def test_user_login(self):
        res = self.client.post('/user/login', {'username': 'yigo', 'password': 'yigo'}, format='json')
        print (res.status_code)
        print (res.content)

