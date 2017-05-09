from django.test import TestCase
from announcement.models import Announcement
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
import json
from rest_framework import status
# Create your tests here.

class Announcement_Authorization_TestCase(TestCase):
    user_with_auth = {'username':'yigo', 'password':'yigo'}
    user_without_auth = {'username':'yigo2', 'password':'yigo2'}

    def setUp(self):
        User.objects.create_user(username = self.user_with_auth['username'],password = self.user_with_auth['password'])
        User.objects.create_user(username = self.user_without_auth['username'],password = self.user_without_auth['password'])
        self.client = APIClient()
        
    def test_create_announcement(self):
        self.client.login(username = self.user_with_auth['username'],password = self.user_with_auth['password'])

        url  = reverse('announcement-list')
        data = {'title': 'This is title', 'content': 'This is content'}
        res = self.client.post(url,data,format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['code'], 0)
        self.assertEqual(js_dic['data'], 'Create announcement success.')

    def test_FET_create_announcement_without_auth(self):
        url  = reverse('announcement-list')
        data = {'title': 'This is title', 'content': 'This is content'}
        res = self.client.post(url,data,format='json')

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['detail'], 'Authentication credentials were not provided.')
    
    def test_update_announcement(self):
        self.client.login(username = self.user_with_auth['username'],password = self.user_with_auth['password'])

        url  = reverse('announcement-list')
        data = {'title': 'This is title', 'content': 'This is content'}
        res = self.client.post(url,data,format='json')

        url  = reverse('announcement-detail', args=['1'])
        data = {'title': 'This is title changed', 'content': 'This is content changed'}
        res = self.client.put(url,data,format='json')

        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['data'], 'Upgrade announcement success.')
        
        res = self.client.get(url,format='json')
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['data']['title'], 'This is title changed')
        self.assertEqual(js_dic['data']['content'], 'This is content changed')
        self.assertEqual(js_dic['data']['owner'], self.user_with_auth['username'])

    def test_update_announcement_without_auth(self):
        self.client.login(username = self.user_with_auth['username'],password = self.user_with_auth['password'])

        url  = reverse('announcement-list')
        data = {'title': 'This is title', 'content': 'This is content'}
        res = self.client.post(url,data,format='json')

        self.client.logout()
        url  = reverse('announcement-detail', args=['1'])
        data = {'title': 'This is title', 'content': 'This is content'}
        res = self.client.put(url,data,format='json')

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['detail'], 'Authentication credentials were not provided.')

        res = self.client.get(reverse('announcement-detail', args=['1']))
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['data']['title'], 'This is title')
        self.assertEqual(js_dic['data']['content'], 'This is content')
        self.assertEqual(js_dic['data']['owner'],  self.user_with_auth['username'])
    
    def test_delete_announcement(self):
        self.client.login(username = self.user_with_auth['username'],password = self.user_with_auth['password'])

        url  = reverse('announcement-list')
        data = {'title': 'This is title', 'content': 'This is content'}
        res = self.client.post(url,data,format='json')

        url  = reverse('announcement-detail', args=['1'])
        res = self.client.delete(url,format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['data'], 'Delete announcement success.')
        
        res = self.client.get(url,format='json')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_announcement_without_auth(self):
        self.client.login(username = self.user_with_auth['username'],password = self.user_with_auth['password'])

        url  = reverse('announcement-list')
        data = {'title': 'This is title', 'content': 'This is content'}
        res = self.client.post(url,data,format='json')

        self.client.logout()
        url  = reverse('announcement-detail', args=['1'])
        data = {'title': 'This is title', 'content': 'This is content'}
        res = self.client.put(url,data,format='json')

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['detail'], 'Authentication credentials were not provided.')

        res = self.client.get(reverse('announcement-detail', args=['1']))
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['data']['title'], 'This is title')
        self.assertEqual(js_dic['data']['content'], 'This is content')
        self.assertEqual(js_dic['data']['owner'],  self.user_with_auth['username'])