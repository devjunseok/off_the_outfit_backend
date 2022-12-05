from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, filters, generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import get_object_or_404
from communities.models import Feed ,Comment,ReComment
from communities.serializers import FeedSerializer, FeedListSerializer, CommentListSerializer, FeedDetailSerializer ,ReCommentListSerializer, SearchProductSerializer



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


class FeedCommentView(APIView): # 댓글 등록 View

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
    def delete(self, request, feed_id, comment_id): # 댓글 삭제
            comment = get_object_or_404(Comment, id= comment_id)
            if request.user == comment.user:
                comment.delete()
                return Response({"message":"댓글 삭제했습니다!"}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message":"권한이 없습니다!"}, status=status.HTTP_403_FORBIDDEN) 

        
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


class CommunitiesFeedLikeView(APIView): # 게시글 좋아요 View
    
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def post(self, request,feed_id ): # 게시글 좋아요
        feed = get_object_or_404(Feed, id=feed_id)
        if request.user in feed.like.all():
            feed.like.remove(request.user)
            return Response({"message":"좋아요 취소했습니다!"}, status=status.HTTP_200_OK)
        else:
            feed.like.add(request.user)
            return Response({"message":"좋아요 했습니다!"}, status=status.HTTP_200_OK)
        

class CommunitiesFeedUnlikeView(APIView): # 게시글 싫아요 View
    
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def post(self, request,feed_id ): # 게시글 싫아요
        feed = get_object_or_404(Feed, id=feed_id)
        if request.user in feed.unlike.all():
            feed.unlike.remove(request.user)
            return Response({"message":"싫어요 취소했습니다!"}, status=status.HTTP_200_OK)
        else:
            feed.unlike.add(request.user)
            return Response({"message":"싫어요 했습니다!"}, status=status.HTTP_200_OK)
        

class CommentLike(APIView): # 댓글 좋아요 View
    
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def post(self, request,comment_id,feed_id ): # 댓글 좋아요
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user in comment.comment_like.all():
            comment.comment_like.remove(request.user)
            return Response({"message":"댓글 좋아요 취소 했습니다!"}, status=status.HTTP_200_OK)
        else:
            comment.comment_like.add(request.user)
            return Response({"message":"댓글 좋아요 했습니다!"}, status=status.HTTP_200_OK)


class ReCommentUpload(APIView): # 대댓글 등록 View
    
    def post(self, request, comment_id, feed_id): #대댓글 등록
        serializer = ReCommentListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, comment_id=comment_id)
            return Response({"message":"대댓글 등록했습니다!"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ReCommentDetailView(APIView):  #대댓글(수정,삭제) View 
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    

    
    def delete(self, request,feed_id, comment_id, recomment_id): # 댓글 삭제
            recomment = get_object_or_404(ReComment, id= recomment_id)
            if request.user == recomment.user:
                recomment.delete()
                return Response({"message":"대댓글 삭제했습니다!"}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message":"권한이 없습니다!"}, status=status.HTTP_403_FORBIDDEN) 


class ReCommentLike(APIView): # 대댓글 좋아요 View
    
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def post(self, request,comment_id,feed_id,recomment_id ): # 댓글 좋아요
        recomment = get_object_or_404(ReComment, id=recomment_id)
        if request.user in recomment.recomment_like.all():
            recomment.recomment_like.remove(request.user)
            return Response({"message":"대댓글 좋아요 취소 했습니다!"}, status=status.HTTP_200_OK)
        else:
            recomment.recomment_like.add(request.user)
            return Response({"message":"대댓글 좋아요 했습니다!"}, status=status.HTTP_200_OK)
    
    



class CommunitySearchView(generics.ListAPIView): # 게시글 검색 View
        
    permission_classes = [permissions.AllowAny]    
    
    queryset = Feed.objects.all()
    serializer_class = FeedListSerializer # 게시글 전체 보기
    # serializer_class = SearchProductSerializer # 상품 검색 시리얼라이즈

    filter_backends = [filters.SearchFilter]
    # 검색 키워드를 지정했을 때, 매칭을 시도할 필드
    # search_fields = ["user","products_name"]
    search_fields = ["user__username"]


