from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from users import serializers
from users.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.serializers import UserSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Create your views here.
class UserView(APIView):
    def post(self, request):  # 회원가입
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"가입완료!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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