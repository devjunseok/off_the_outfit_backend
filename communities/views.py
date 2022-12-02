from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework import status, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from communities.serializers import  CommentListSerializer
from communities.models import  Comment

# Create your views here.
class AllFeedView(APIView):
    pass

class FeedCommentView(APIView): # 댓글 등록 View
    
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, feed_id): # 댓글 등록
        serializer = CommentListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, feed_id=feed_id)
            return Response({"message":"댓글 등록했습니다!"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
            
class FeedCommentDetailView(APIView):  #댓글(수정,삭제) View 
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def put(self, request, feed_id, comment_id): # 댓글 수정
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            serializer = CommentListSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"댓글 수정했습니다!"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"권한이 없습니다!"}, status=status.HTTP_403_FORBIDDEN)
            
    def delete(self, request, feed_id, comment_id): # 댓글 삭제
        comment = get_object_or_404(Comment, id= comment_id)
        if request.user == comment.user:
            comment.delete()
            return Response({"message":"댓글 삭제했습니다!"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message":"권한이 없습니다!"}, status=status.HTTP_403_FORBIDDEN)  