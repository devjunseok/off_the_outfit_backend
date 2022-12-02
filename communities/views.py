from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import get_object_or_404

from communities.models import Feed
from communities.serializers import FeedSerializer, FeedListSerializer, FeedDetailSerializer


# Create your views here.

class ArticlesFeedView(APIView):  # 게시글 전체보기, 등록 View
    
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request): # 게시글 전체 보기
        articles = Feed.objects.all().order_by('-created_at')
        serializer = FeedListSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

        
    def post(self, request): # 게시글 등록
        serializer = FeedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"message":"게시글이 등록되었습니다!"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class ArticlesFeedDetailView(APIView): #게시글 상세조회, 수정, 삭제 View
    
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request, feed_id): # 게시글 상세 조회
        feed = get_object_or_404(Feed, id=feed_id)
        serializer = FeedDetailSerializer(feed)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, feed_id): # 게시글 수정
        feed = get_object_or_404(Feed, id= feed_id)
        if request.user == feed.user:
            serializer = FeedSerializer(feed, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"게시글이 수정되었습니다!"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"권한이 없습니다!"}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, feed_id): # 게시글 삭제
        feed = get_object_or_404(Feed, id= feed_id)
        if request.user == feed.user:
            feed.delete()
            return Response({"message":"게시글이 삭제되었습니다!"},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)
    
