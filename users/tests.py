from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
import re

class UserRegistrationTest(APITestCase): # 회원가입 테스트
    def test_registration(self):  #회원가입 성공 테스트
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
        
        
    def test_registration_failed_username_blank(self):  #회원가입 실패 테스트(username 입력 안했을 때)
        url = reverse("user_view")   # url name
        user_data = {
                "username":"",
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
        self.assertEqual(response.status_code, 400)
        
    
    def test_registration_failed_username_validation(self):  #회원가입 실패 테스트(username 유효성 검사 통과 X, username에 특수문자 들어가 있을 때)
        url = reverse("user_view")   # url name
        user_data = {
                "username":"testuser@",
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
        self.assertEqual(response.status_code, 400)
        
    def test_registration_failed_username_unique(self):  #회원가입 실패 테스트(username 중복)
        User.objects.create_user("test@test.com", "testuser", "tester", "password123@") # 이메일, 유저네임, 닉네임, 패스워드 순(create_user 인자값)
        url = reverse("user_view")   # url name
        user_data = {
                "username":"testuser",
                "email":"test1@test.com",
                "nickname":"tester1",
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
        self.assertEqual(response.status_code, 400)

    def test_registration_failed_email_blank(self):  #회원가입 실패 테스트(email 입력 안했을 때)
        url = reverse("user_view")   # url name
        user_data = {
                "username":"testuser",
                "email":"",
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
        self.assertEqual(response.status_code, 400)
    
    
    def test_registration_failed_email_validation(self):  #회원가입 실패 테스트(email 유효성 검사 테스트 미통과, 맞지 않는 이메일 형식)
        url = reverse("user_view")   # url name
        user_data = {
                "username":"testuser",
                "email":"test-test.com",
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
        self.assertEqual(response.status_code, 400)
    
    def test_registration_failed_email_unique(self):  #회원가입 실패 테스트(email 중복)
        User.objects.create_user("test@test.com", "testuser", "tester", "password123@") # 이메일, 유저네임, 닉네임, 패스워드 순(create_user 인자값)
        url = reverse("user_view")   # url name
        user_data = {
                "username":"testuser1",
                "email":"test@test.com",
                "nickname":"tester1",
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
        self.assertEqual(response.status_code, 400)
    
    def test_registration_failed_nickname_blank(self):  #회원가입 실패 테스트(nickname 입력 안했을 때)
        url = reverse("user_view")   # url name
        user_data = {
                "username":"testuser",
                "email":"test@test.com",
                "nickname":"",
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
        self.assertEqual(response.status_code, 400)
    
    def test_registration_failed_nickname_validation(self):  #회원가입 실패 테스트(nickname 유효성 검사 통과x, 닉네임에 특수문자 포함 되었을 때,)
        url = reverse("user_view")   # url name
        user_data = {
                "username":"testuser",
                "email":"test@test.com",
                "nickname":"tester@",
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
        self.assertEqual(response.status_code, 400)
    
    def test_registration_failed_nickname_unique(self):  #회원가입 실패 테스트(nickname 중복)
        User.objects.create_user("test@test.com", "testuser", "tester", "password123@") # 이메일, 유저네임, 닉네임, 패스워드 순(create_user 인자값)
        url = reverse("user_view")   # url name
        user_data = {
                "username":"testuser1",
                "email":"test1@test.com",
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
        self.assertEqual(response.status_code, 400)
        
    def test_registration_failed_address_blank(self):  #회원가입 실패 테스트(address 미입력)
        url = reverse("user_view")   # url name
        user_data = {
                "username":"testuser",
                "email":"test@test.com",
                "nickname":"tester",
                "address":"",
                "gender":"M",
                "height":"1",
                "weight":"2",
                "date_of_birth":"1998-06-16",
                "password":"password123@",
                "password2":"password123@",
                "term_agree":"True"
            }
        response = self.client.post(url, user_data)  # APITestCase의 기본적인 세팅
        self.assertEqual(response.status_code, 400)
    
    def test_registration_failed_address_validation(self):  #회원가입 실패 테스트(address 유효성 검사 테스트 미통과, 주소에 특수문자 포함)
        url = reverse("user_view")   # url name
        user_data = {
                "username":"testuser",
                "email":"test@test.com",
                "nickname":"tester",
                "address":"seoul@",
                "gender":"M",
                "height":"1",
                "weight":"2",
                "date_of_birth":"1998-06-16",
                "password":"password123@",
                "password2":"password123@",
                "term_agree":"True"
            }
        response = self.client.post(url, user_data)  # APITestCase의 기본적인 세팅
        self.assertEqual(response.status_code, 400)
    
    def test_registration_failed_height_blank(self):  #회원가입 실패 테스트(height 미입력)
        url = reverse("user_view")   # url name
        user_data = {
                "username":"testuser",
                "email":"test@test.com",
                "nickname":"tester",
                "address":"seoul",
                "gender":"M",
                "height":"",
                "weight":"2",
                "date_of_birth":"1998-06-16",
                "password":"password123@",
                "password2":"password123@",
                "term_agree":"True"
            }
        response = self.client.post(url, user_data)  # APITestCase의 기본적인 세팅
        self.assertEqual(response.status_code, 400)
    
    def test_registration_failed_height_validation(self):  #회원가입 실패 테스트(height 유효성 검사 테스트 미통과, height에 숫자 제외 다른 문자 입력)
        url = reverse("user_view")   # url name
        user_data = {
                "username":"testuser",
                "email":"test@test.com",
                "nickname":"tester",
                "address":"seoul",
                "gender":"M",
                "height":"height",
                "weight":"2",
                "date_of_birth":"1998-06-16",
                "password":"password123@",
                "password2":"password123@",
                "term_agree":"True"
            }
        response = self.client.post(url, user_data)  # APITestCase의 기본적인 세팅
        self.assertEqual(response.status_code, 400)
    
    def test_registration_failed_weight_blank(self):  #회원가입 실패 테스트(weight 미입력)
        url = reverse("user_view")   # url name
        user_data = {
                "username":"testuser",
                "email":"test@test.com",
                "nickname":"tester",
                "address":"seoul",
                "gender":"M",
                "height":"1",
                "weight":"",
                "date_of_birth":"1998-06-16",
                "password":"password123@",
                "password2":"password123@",
                "term_agree":"True"
            }
        response = self.client.post(url, user_data)  # APITestCase의 기본적인 세팅
        self.assertEqual(response.status_code, 400)
    
    def test_registration_failed_weight_validation(self):  #회원가입 실패 테스트(weight 유효성 검사 테스트 미통과, weight에 숫자 제외 다른 문자 입력)
        url = reverse("user_view")   # url name
        user_data = {
                "username":"testuser",
                "email":"test@test.com",
                "nickname":"tester",
                "address":"seoul",
                "gender":"M",
                "height":"1",
                "weight":"weight",
                "date_of_birth":"1998-06-16",
                "password":"password123@",
                "password2":"password123@",
                "term_agree":"True"
            }
        response = self.client.post(url, user_data)  # APITestCase의 기본적인 세팅
        self.assertEqual(response.status_code, 400)
    
    def test_registration_failed_date_of_birth_validation(self):  #회원가입 실패 테스트(date_of_birth 유효성 검사 통과 x)
        url = reverse("user_view")   # url name
        user_data = {
                "username":"testuser",
                "email":"test@test.com",
                "nickname":"tester",
                "address":"seoul",
                "gender":"M",
                "height":"1",
                "weight":"1",
                "date_of_birth":"19980616",
                "password":"password123@",
                "password2":"password123@",
                "term_agree":"True"
            }
        response = self.client.post(url, user_data)  # APITestCase의 기본적인 세팅
        self.assertEqual(response.status_code, 400)
    
    def test_registration_failed_password_password2_diffrenrt(self):  #회원가입 실패 테스트(password, password2 일치하지 않을 때.)
        url = reverse("user_view")   # url name
        user_data = {
                "username":"testuser",
                "email":"test@test.com",
                "nickname":"tester",
                "address":"seoul",
                "gender":"M",
                "height":"1",
                "weight":"1",
                "date_of_birth":"1998-06-16",
                "password":"password123@",
                "password2":"password1234@",
                "term_agree":"True"
            }
        response = self.client.post(url, user_data)  # APITestCase의 기본적인 세팅
        self.assertEqual(response.status_code, 400)
    
    def test_registration_failed_password_validation(self):  #회원가입 실패 테스트(password 유효성 검사 통과 x)
        url = reverse("user_view")   # url name
        user_data = {
                "username":"testuser",
                "email":"test@test.com",
                "nickname":"tester",
                "address":"seoul",
                "gender":"M",
                "height":"1",
                "weight":"1",
                "date_of_birth":"1998-06-16",
                "password":"password123",
                "password2":"password123",
                "term_agree":"True"
            }
        response = self.client.post(url, user_data)  # APITestCase의 기본적인 세팅
        self.assertEqual(response.status_code, 400)
    
    def test_registration_failed_term_aggree_disagree(self):  #회원가입 실패 테스트(개인정보 약관 동의 미체크)
        url = reverse("user_view")   # url name
        user_data = {
                "username":"testuser",
                "email":"test@test.com",
                "nickname":"tester",
                "address":"seoul",
                "gender":"M",
                "height":"1",
                "weight":"1",
                "date_of_birth":"1998-06-16",
                "password":"password123@",
                "password2":"password123@",
                "term_agree":"False"
            }
        response = self.client.post(url, user_data)  # APITestCase의 기본적인 세팅
        self.assertEqual(response.status_code, 400)

class LoginUserTest(APITestCase): # 로그인 테스트 코드 작성
    def setUp(self):  # DB 셋업
        
        self.data = {'username': 'testuser', 'password': 'password123@'}
        self.user = User.objects.create_user("test@test.com", "testuser", "tester", "password123@")
    
    def test_login(self):   # 로그인 테스트
        response = self.client.post(reverse('token_obtain_pair'), self.data)
        self.assertEqual(response.status_code, 200)