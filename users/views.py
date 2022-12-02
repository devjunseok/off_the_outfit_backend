from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from users import serializers
from users.models import User
from users.serializers import UserSerializer, CustomTokenObtainPairSerializer, UserProfileSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Create your views here.
class UserView(APIView):
    permission_classes = [AllowAny]
    
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


class CustomTokenObtainPairView(TokenObtainPairView): # jwt payload 커스텀
    serializer_class = CustomTokenObtainPairSerializer