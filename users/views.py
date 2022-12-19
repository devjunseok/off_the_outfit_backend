import os
import requests

from datetime import datetime
from django.shortcuts import redirect
from django.http import JsonResponse

from users.models import User
from users.serializers import UserSerializer, CustomTokenObtainPairSerializer , UserProfileSerializer, PasswordChangeSerializer

from dj_rest_auth.registration.views import SocialLoginView

from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions, filters, generics
from rest_framework.decorators import api_view
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.db.models import Q

from json.decoder import JSONDecodeError

from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

BASE_URL = 'http://127.0.0.1:8000/'
KAKAO_CALLBACK_URI = BASE_URL + 'users/kakao/callback/'


# 회원정보 전체 보기, 회원가입, 회원정보 수정, 회원탈퇴 View
class UserView(APIView): 
    permission_classes = [permissions.AllowAny]
    
    # 회원정보 전체 보기
    def get(self, request):
        user = User.objects.filter(~Q(id=request.user.id)) # request한 유저를 제외
        serializer = UserProfileSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 회원가입
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"가입완료!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 회원정보 수정
    def put(self, request): 
        user = get_object_or_404(User, id=request.user.id)
        if user == request.user:
            serializer = UserSerializer(user, data=request.data, partial=True, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"변경되었습니다!","nickname":user.nickname}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"권한이 없습니다!"}, status=status.HTTP_403_FORBIDDEN)

    # 회원탈퇴
    def delete(self, request):
        if request.user.is_authenticated:
            request.user.delete()
            return Response({"message":"탈퇴되었습니다!"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message":"권한이 없습니다!"}, status=status.HTTP_403_FORBIDDEN)
        
# TokenObtainPariView 커스텀 View
class CustomTokenObtainPairView(TokenObtainPairView): 
    serializer_class = CustomTokenObtainPairSerializer

# 비밀번호 변경 View
class PasswordChangeView(APIView): 
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    # 비밀번호 수정
    def put(self, request): 
        user = get_object_or_404(User, id=request.user.id)
        if request.user == user:
            serializer = PasswordChangeSerializer(user, data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"비밀번호가 변경되었습니다!"}, status=status.HTTP_200_OK)
        
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"권한이 없습니다!"}, status=status.HTTP_403_FORBIDDEN)
    
# follow View
class FollowView(APIView): 
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    # follow
    def post (self, request, user_id):
        you = get_object_or_404(User, id=user_id)
        me = request.user
        if me == you:

            return Response({"message":"스스로를 follow 할 수 없습니다"})
        else:
            if me in you.followers.all():
                you.followers.remove(me)
                return Response({"message":"unfollow했습니다."}, status=status.HTTP_200_OK)
            else:
                you.followers.add(me)
                return Response({"message":"follow했습니다."}, status=status.HTTP_200_OK)
            
# 회원정보 상세 조회 View                
class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = UserProfileSerializer(user)  
        return Response(serializer.data)
    
# 유저 검색 View    
class UserSearchView(generics.ListAPIView): 
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]    
    
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer # 유저 시리얼라이즈

    filter_backends = [filters.SearchFilter]
    # 검색 키워드를 지정했을 때, 매칭을 시도할 필드

    search_fields = ["username"]

# 출석 포인트 View (하루에 한번 가능)
class GetPointView(APIView): 
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, user_id):
        now = datetime.today().strftime("%Y-%m-%d")
        user= get_object_or_404(User, id=user_id)
        if user == request.user:
            if user.click_time == now:   
                return Response({"message":"이미 출석을 하셨습니다."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user.click_time = now
                user.point += 5
                user.save()
            return Response({"message":"출석점수 1점을 획득하셨습니다."}, status=status.HTTP_200_OK)
        return Response({"message":"권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
    
# 팔로잉 유저 조회 View
class GetFollowingsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request, user_id):
        users = User.objects.filter(followers = user_id)
        serializer = UserProfileSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# 팔로워 유저 조회 View
class GetFollowersView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request, user_id):
        users = User.objects.filter(followings = user_id)
        serializer = UserProfileSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SocialLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, requset):
        client_id = "75756f04ae592ba908cfcfcdac87df17"
        return redirect(f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={'users/social/'}&response_type=code&scope=account_email")
    
    
    def post(self, request):
        code = request.data.get('code')
        token_request = requests.post(
                "https://kauth.kakao.com/oauth/token",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data={
                    "grant_type": "authorization_code",
                    "client_id": "75756f04ae592ba908cfcfcdac87df17",
                    "redirect_uri": "http://http://127.0.0.1:8000//",
                    "code": code,
                },
            )
        token_response_json = token_request.json()
        access_token = token_response_json.get("access_token")
        
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}", "Content-type": "application/x-www-form-urlencoded;charset=utf-8"})
        profile_json = profile_request.json()
        
        email = profile_json.get('kakao_account')['email']
        nickname = profile_json.get('properties')['nickname']
        profile_image = profile_json.get('properties')['profile_image']
        
        try:
            user = User.objects.get(email=email)
            social_user = SocialAccount.objects.filter(user=user).first()
            
            if social_user:
                if social_user.provider !="kakao":
                    return Response({"error": "카카오로 가입한 유저가 아닙니다."}, status=status.HTTP_400_BAD_REQUEST)
                
                refresh = RefreshToken.for_user(user)
                return Response({'refresh': str(refresh), 'access': str(refresh.access_token), "msg" : "로그인 성공"}, status=status.HTTP_200_OK)
            
            if social_user is None:
                    return Response({"error":"이메일이 존재하지만 , 소셜유저가 아닙니다"}, status=status.HTTP_400_BAD_REQUEST)
            
        
        except User.DoesNotExist:
            new_user = User.objects.create(
                username=nickname,
                nickname=nickname,
                email=email,
            )
            
            SocialAccount.objects.create(
                user_id=new_user.id,
                uid=new_user.email,
                provider="kakao",
            )
            
            refresh = RefreshToken.for_user(new_user)
            return Response({'refresh': str(refresh), 'access': str(refresh.access_token), "msg" : "회원가입 성공"}, status=status.HTTP_201_CREATED)
    

def kakao_login(request):
    client_id = os.environ.get("SOCIAL_AUTH_KAKAO_CLIENT_ID")
    return redirect(f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code&scope=account_email")

@api_view(['POST'])
def kakao_callback(request): # 카카오 소셜 로그인 callback 함수
    client_id = os.environ.get("SOCIAL_AUTH_KAKAO_CLIENT_ID")
    code = request.GET.get("code")
    redirect_uri = KAKAO_CALLBACK_URI

    # code로 access token 요청
    token_request = requests.get(f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={KAKAO_CALLBACK_URI}&code={code}")
    token_response_json = token_request.json()
    error = token_response_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    access_token = token_response_json.get("access_token")
    
    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"})
    profile_json = profile_request.json()
    kakao_account = profile_json.get('kakao_account')


    email = kakao_account.get("email", None) # 이메일!
    
    try:
        user = User.objects.get(email=email)
        social_user = SocialAccount.objects.get(user=user)
        
        if social_user:
            # 소셜계정이 카카오가 아닌 다른 소셜계정으로 가입한 유저일때(구글, 네이버)
            if social_user.provider != "kakao":
                return Response({"error": "카카오로 가입한 유저가 아닙니다."}, status=status.HTTP_400_BAD_REQUEST)

            refresh = RefreshToken.for_user(user)
            return Response({'refresh': str(refresh), 'access': str(refresh.access_token), "msg" : "로그인 성공"}, status=status.HTTP_200_OK)
        
        if social_user is None:
            return Response({"error": "이메일이 존재하지만, 소셜유저가 아닙니다."}, status=status.HTTP_400_BAD_REQUEST)

        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}users/kakao/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
        accept_json = accept.json()
        accept_json.pop('user', None)
        return JsonResponse(accept_json)
        # return Response({'message': '로그인 되었습니다!'}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}users/kakao/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
        # user의 pk, email, first name, last name과 Access Token, Refresh token 가져옴
        accept_json = accept.json()
        accept_json.pop('user', None)
        # return JsonResponse(accept_json)
        return Response({'message': '가입 되었습니다!'}, status=status.HTTP_200_OK)

class KakaoLogin(SocialLoginView): 
    adapter_class = kakao_view.KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = KAKAO_CALLBACK_URI
    
            
            
                
        
        
