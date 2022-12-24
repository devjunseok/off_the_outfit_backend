from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User

from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY
from PIL import Image
import tempfile

# 임시 이미지파일 생성
def get_temporary_image(temp_file):
    size = (200, 200)
    color = (255, 0, 0, 0)
    image = Image.new("RGBA", size, color)
    image.save(temp_file, 'png')
    return temp_file

# 게시글 작성 테스트
class ArticleCreateTest(APITestCase):
    @classmethod
    # 더미데이터 classmethod로 생성
    def setUpTestData(cls):
        cls.user_data = {'username': 'testuser', 'password': 'password123@'}
        cls.article_data = {'tags': '#tag', 'content': 'some content'}
        cls.user = User.objects.create_user("test@test.com", "testuser", "tester", "password123@")
    
    ## 엑세스 토큰을 받아옴   
    def setUp(self):
        self.access_token = self.client.post(reverse('token_obtain_pair'), self.user_data).data['access']  
    
    def test_create_feed_success(self):
        #임시 이미지 파일 생성
        temp_file = tempfile.NamedTemporaryFile()
        temp_file.name = "image.png"
        image_file = get_temporary_image(temp_file)
        image_file.seek(0)
        
        #전송
        response = self.client.post(
            path=reverse("feed_list_view"),
            data=encode_multipart(data = self.article_data, boundary=BOUNDARY),
            content_type=MULTIPART_CONTENT,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        self.assertEqual(response.data["message"], "게시글이 등록되었습니다!")
        self.assertEqual(response.status_code, 200)