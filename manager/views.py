from datetime import datetime, timedelta

from communities.serializers import FeedListSerializer
from communities.models import Feed 

from users.models import User
from users.serializers import UserProfileSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import get_object_or_404

# 일정횟수 신고당한 게시글 열람 View
class ReportFeedView(APIView): 
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    # 신고당한 게시글 열람
    def get(self, request):  
        user = get_object_or_404(User, id= request.user.id)
        feed = Feed.objects.filter(report_point__ge=1)
        if user.roles == 'ROLE_SUPER':
            serializer = FeedListSerializer(feed, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message":"권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

# 관리자 권한 게시글 관리 View
class FeedManageView(APIView): 
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    # 신고 횟수 초기화
    def post(self, request, feed_id): 
        user = get_object_or_404(User, id=request.user.id)
        feed = get_object_or_404(Feed, id=feed_id)
        if user.roles == 'ROLE_SUPER':
            feed.report_point = 0
            feed.save()
            return Response({"message":"신고 횟수를 초기화했습니다!"}, status=status.HTTP_200_OK)
        return Response({"message":"권한이 없습니다!"}, status=status.HTTP_400_BAD_REQUEST)
        
    # 신고당한 게시글 삭제
    def delete(self, request, feed_id):
        user = get_object_or_404(User, id=request.user.id)
        feed = get_object_or_404(Feed, id=feed_id)
        if user.roles == 'ROLE_SUPER':
            feed.delete()
            return Response({"message":"게시글 삭제했습니다!"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message":"권한이 없습니다!"}, status=status.HTTP_400_BAD_REQUEST)

# 관리자 권한 유저 목록 열람 View
class UserManageView(APIView): 
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    # 회원정보 전체 보기
    def get(self, request): 
        user = get_object_or_404(User, id=request.user.id)
        all_user = User.objects.all()
        serializer = UserProfileSerializer(all_user, many=True)
        if user.roles == 'ROLE_SUPER':
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message":"권한이 없습니다!"}, status=status.HTTP_400_BAD_REQUEST)
    
    
# 관리자 권한 유저 목록 열람 View
class UserManageDetailView(APIView): 
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    # 특정 회원 삭제   
    def delete(self, request, user_id): 
        user = get_object_or_404(User, id=request.user.id)
        all_user = get_object_or_404(User, id=user_id)
        if user.roles == 'ROLE_SUPER':
            if user.id == all_user.id:
                return Response({"message":"본인을 삭제할 수 없습니다!"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                all_user.delete()
                return Response({"message":"회원을 삭제했습니다!"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message":"권한이 없습니다!"}, status=status.HTTP_400_BAD_REQUEST)

# 휴면 유저 삭제
class UserDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def delete(self, request):
        User.objects.filter(last_login__lte=datetime.now()-timedelta(days=365)).delete()
        return Response({"message":"회원을 삭제했습니다!"}, status=status.HTTP_204_NO_CONTENT)