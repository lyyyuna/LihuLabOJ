import json
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from announcement.models import Announcement


class Announcement_Pagination_TestCase(TestCase):
    user_with_auth   = {'username':'yigo', 'password':'yigo','is_staff':'True'}
    announcement_num = 20
    
    def setUp(self):
        user = User.objects.create_user(username = self.user_with_auth['username'],
                                        password = self.user_with_auth['password'],
                                        is_staff = self.user_with_auth['is_staff'])
        num = range(self.announcement_num)
        for i in num:
            i_str = str(i)
            Announcement.objects.create(title = "title"+i_str,
                                        content ="content"+i_str,
                                        owner = user)
        self.client = APIClient()
        
    def test_list_1st_page_announcements(self):
        url  = reverse('announcement-list')
        res = self.client.get(url,format='json')        
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['count'], self.announcement_num)
        self.assertEqual(js_dic['next'], 'http://testserver'+url + '?page=2')
        self.assertEqual(js_dic['previous'], None)

    def test_list_2nd_page_announcements(self):
        url  = reverse('announcement-list')
        res = self.client.get('http://testserver' + url + '?page=2',format='json')        
        self.assertEqual(res.status_code, 200)
        js_dic = json.loads(res.content.decode('utf-8'))
        self.assertEqual(js_dic['count'], self.announcement_num)
        self.assertEqual(js_dic['next'], None)
        self.assertEqual(js_dic['previous'], 'http://testserver'+url)

    def test_FET_list_3th_page_announcements(self):
        url  = reverse('announcement-list')
        res = self.client.get('http://testserver' + url + '?page=3',format='json')        
        self.assertEqual(res.status_code,status.HTTP_404_NOT_FOUND)

    def test_FET_list_0_page_announcements(self):
        url  = reverse('announcement-list')
        res = self.client.get('http://testserver' + url + '?page=0',format='json')        
        self.assertEqual(res.status_code,status.HTTP_404_NOT_FOUND)

    def test_FET_list_minus_1_page_announcements(self):
        url  = reverse('announcement-list')
        res = self.client.get('http://testserver' + url + '?page=-1',format='json')        
        self.assertEqual(res.status_code,status.HTTP_404_NOT_FOUND)
