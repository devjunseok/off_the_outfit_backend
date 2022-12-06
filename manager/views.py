from communities.serializers import FeedListSerializer

from communities.models import Feed 

from users.models import User


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, filters, generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import get_object_or_404

# Create your views here.
class ReportFeedView(APIView): # 일정횟수 신고당한 게시글 열람 View
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request):  # 신고당한 게시글 열람
        user = get_object_or_404(User, id= request.user.id)
        feed = Feed.objects.filter(report_point__gt=1)
        if user.roles == 'ROLE_SUPER':
            serializer = FeedListSerializer(feed, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message":"권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

class ReportFeedDetailView(APIView): # 신고당한 게시글 관리 View(관리자 권한)
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def post(self, request, feed_id): # 신고 횟수 초기화
        user = get_object_or_404(User, id=request.user.id)
        feed = get_object_or_404(Feed, id=feed_id)
        if user.roles == 'ROLE_SUPER':
            feed.report_point = 0
            feed.save()
            return Response({"message":"신고 횟수를 초기화했습니다!"}, status=status.HTTP_200_OK)
        return Response({"message":"권한이 없습니다!"}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, feed_id): # 신고당한 게시글 삭제
        user = get_object_or_404(User, id=request.user.id)
        feed = get_object_or_404(Feed, id=feed_id)
        if user.roles == 'ROLE_SUPER':
            feed.delete()
            return Response({"message":"게시글 삭제했습니다!"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message":"권한이 없습니다!"}, status=status.HTTP_400_BAD_REQUEST)