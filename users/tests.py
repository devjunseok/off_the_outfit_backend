from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
import re

class UserRegistrationTest(APITestCase):
    def test_registration_success_case(self):  #회원가입 성공 테스트
        url = reverse("user_view")   # url name
        user_data = {
                "username":"testuser",
                "email":"test@test.com",
                "nickname":"tester",
                "address":"seoul",
                "gender":"M",
                "height":"1",
                "weight":"2",
                "date_of_birth":"1998-06-16",
                "password":"password123@",
                "password2":"password123@",
                "term_agree":"True"
            }
        response = self.client.post(url, user_data)  # APITestCase의 기본적인 세팅
        self.assertEqual(response.status_code, 201)
        
        
    def test_registration_blank_username_fail_case(self):  #회원가입 실패 테스트(username 입력 안했을 때)
        url = reverse("user_view")   # url name
        user_data = {
                "username":"",
                "email":"test@test.com",
                "nickname":"tester",
                "address":"seoul",
                "gender":"M",
                "height":"1",
                "weight":"2",
                "date_of_birth":"0000-00-00",
                "password":"password123@",
                "password2":"password123@",
                "term_agree":"True"
            }
        response = self.client.post(url, user_data)  # APITestCase의 기본적인 세팅
        self.assertEqual(response.status_code, 400)