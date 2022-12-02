from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions, filters, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from users import serializers
from users.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.serializers import UserSerializer, CustomTokenObtainPairSerializer , UserProfileSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Create your views here.
class UserView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request): # 회원정보 전체 보기
        user = get_object_or_404(User, id=request.user.id)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def post(self, request):  # 회원가입
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"가입완료!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def put(self, request): # 회원정보 수정
        user = get_object_or_404(User, id=request.user.id)
        if user == request.user:
            serializer = UserSerializer(user, data=request.data, partial=True, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"변경되었습니다!"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"권한이 없습니다!"}, status=status.HTTP_403_FORBIDDEN)


    def delete(self, request): # 회원탈퇴
        if request.user.is_authenticated:
            request.user.delete()
            return Response({"message":"탈퇴되었습니다!"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message":"권한이 없습니다!"}, status=status.HTTP_403_FORBIDDEN)

class CustomTokenObtainPairView(TokenObtainPairView): # jwt payload 커스텀
    serializer_class = CustomTokenObtainPairSerializer




class FollowView(APIView): # follow View

    


    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    

    def post (self, request, user_id):
        you = get_object_or_404(User, id=user_id)
        me = request.user
        if me == you:

            return Response({"message":"스스로를 follow 할 수 없습니다"})
        else:
            if me in you.followings.all():
                you.followings.remove(me)
                return Response({"message":"unfollow했습니다."}, status=status.HTTP_200_OK)
            else:
                you.followings.add(me)
                return Response({"message":"follow했습니다."}, status=status.HTTP_200_OK)
                
class ProfileView(APIView):  # 회원정보 조회

    
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = UserProfileSerializer(user)  
        return Response(serializer.data)
    

class UserSearchView(generics.ListAPIView): # 유저 검색 View
        
    permission_classes = [permissions.AllowAny]    
    
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer # 유저 시리얼라이즈

    filter_backends = [filters.SearchFilter]
    # 검색 키워드를 지정했을 때, 매칭을 시도할 필드

    search_fields = ["username"]
