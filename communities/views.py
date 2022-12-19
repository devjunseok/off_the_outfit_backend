from communities.serializers import FeedSerializer, FeedListSerializer, CommentListSerializer, FeedDetailSerializer ,ReCommentListSerializer, ReportSerializer, SearchWordSerializer
from communities.models import Feed ,Comment,ReComment, SearchWord

from users.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, filters, generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated


# 게시글 전체보기, 등록 View
class ArticlesFeedView(APIView):  
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    # 게시글 전체 보기
    def get(self, request): 
        articles = Feed.objects.all().order_by('-created_at')
        serializer = FeedListSerializer(articles, many=True)        
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 게시글 등록
    def post(self, request):
        serializer = FeedSerializer(data=request.data,)
        me= User.objects.get(id=request.user.id)
        if serializer.is_valid():
            if me == request.user:
                me.point += 10
                me.save()
                serializer.save(user=request.user)
            return Response({"message":"게시글이 등록되었습니다!"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 댓글 등록 View
class FeedCommentView(APIView): 
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    # 댓글 등록
    def post(self, request, feed_id): 
        serializer = CommentListSerializer(data=request.data)
        me= User.objects.get(id=request.user.id)
        if serializer.is_valid():
            if me == request.user:
                me.point += 1
                me.save()
                serializer.save(user=request.user, feed_id=feed_id)
            return Response({"message":"댓글 등록했습니다!"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#댓글(수정,삭제) View     
class FeedCommentDetailView(APIView): 
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    # 댓글 수정
    def put(self, request, feed_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            serializer = CommentListSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"댓글 수정했습니다!"}, status=status.HTTP_200_OK)
    
    # 댓글 삭제   
    def delete(self, request, feed_id, comment_id): 
            comment = get_object_or_404(Comment, id= comment_id)
            feed_user = get_object_or_404(User, id=request.user.id)
    
            if request.user == comment.user:
                feed_user.point -=1
                feed_user.save()
                comment.delete()
                return Response({"message":"댓글 삭제했습니다!"}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message":"권한이 없습니다!"}, status=status.HTTP_403_FORBIDDEN) 

    
#게시글 상세조회, 수정, 삭제 View    
class ArticlesFeedDetailView(APIView): 
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    # 게시글 상세 조회
    def get(self, request, feed_id): 
        feed = get_object_or_404(Feed, id=feed_id)
        serializer = FeedDetailSerializer(feed)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 게시글 수정
    def put(self, request, feed_id): 
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
            
    # 게시글 삭제
    def delete(self, request, feed_id):
        feed = get_object_or_404(Feed, id= feed_id)
        feed_user = get_object_or_404(User, id=request.user.id)
        
        if request.user == feed.user:
            feed_user.point -=10
            feed_user.save()
            feed.delete()
            return Response({"message":"게시글이 삭제되었습니다!"},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)

# 게시글 좋아요 View
class CommunitiesFeedLikeView(APIView): 
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    # 게시글 좋아요
    def post(self, request,feed_id ): 
        feed = get_object_or_404(Feed, id=feed_id)
        feed_user = User.objects.get(id=feed.user.pk)
        
        if request.user in feed.like.all():
            feed_user.point -=1
            feed_user.save()
            feed.like.remove(request.user)
            return Response({"message":"좋아요 취소했습니다!"}, status=status.HTTP_200_OK)
        else:
            feed_user.point +=1
            feed_user.save()
            feed.like.add(request.user)
            return Response({"message":"좋아요 했습니다!"}, status=status.HTTP_200_OK)
        
# 게시글 싫어요 View
class CommunitiesFeedUnlikeView(APIView): 
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    # 게시글 싫어요
    def post(self, request,feed_id ): 
        feed = get_object_or_404(Feed, id=feed_id)
        if request.user in feed.unlike.all():
            feed.unlike.remove(request.user)
            return Response({"message":"싫어요 취소했습니다!"}, status=status.HTTP_200_OK)
        else:
            feed.unlike.add(request.user)
            return Response({"message":"싫어요 했습니다!"}, status=status.HTTP_200_OK)
        
# 댓글 좋아요 View
class CommentLike(APIView): 
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    # 댓글 좋아요
    def post(self, request,comment_id,feed_id ): 
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user in comment.comment_like.all():
            comment.comment_like.remove(request.user)
            return Response({"message":"댓글 좋아요 취소 했습니다!"}, status=status.HTTP_200_OK)
        else:
            comment.comment_like.add(request.user)
            return Response({"message":"댓글 좋아요 했습니다!"}, status=status.HTTP_200_OK)

# 대댓글 등록 View
class ReCommentUpload(APIView): 
    
    #대댓글 등록
    def post(self, request, comment_id, feed_id): 
        serializer = ReCommentListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, comment_id=comment_id)
            return Response({"message":"대댓글 등록했습니다!"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#대댓글(수정,삭제) View 
class ReCommentDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    # 대댓글 삭제
    def delete(self, request,feed_id, comment_id, recomment_id): 
            recomment = get_object_or_404(ReComment, id= recomment_id)
            if request.user == recomment.user:
                recomment.delete()
                return Response({"message":"대댓글 삭제했습니다!"}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message":"권한이 없습니다!"}, status=status.HTTP_403_FORBIDDEN) 

# 대댓글 좋아요 View
class ReCommentLike(APIView): 
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    # 댓글 좋아요
    def post(self, request,comment_id,feed_id,recomment_id ): 
        recomment = get_object_or_404(ReComment, id=recomment_id)
        if request.user in recomment.recomment_like.all():
            recomment.recomment_like.remove(request.user)
            return Response({"message":"대댓글 좋아요 취소 했습니다!"}, status=status.HTTP_200_OK)
        else:
            recomment.recomment_like.add(request.user)
            return Response({"message":"대댓글 좋아요 했습니다!"}, status=status.HTTP_200_OK)
    
# 게시글 검색 View
class CommunitySearchView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    queryset = Feed.objects.all()
    serializer_class = FeedListSerializer # 게시글 전체 보기
    # serializer_class = SearchProductSerializer # 상품 검색 시리얼라이즈

    filter_backends = [filters.SearchFilter]
    # 검색 키워드를 지정했을 때, 매칭을 시도할 필드
    # search_fields = ["user","products_name"]
    search_fields = ["user__nickname","content","tags__name"]
    
    # 검색어 저장 추가
    def get(self, request, *args, **kwargs): 
        search = SearchWord()
        word = request.GET.get('search')
        search.word = word
        search.save()
        return self.list(request, *args, **kwargs)

# 게시글 신고 View
class ReportView(APIView): 
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    
    def post(self, request, feed_id):
        serializer = ReportSerializer(data=request.data)
        feed= get_object_or_404(Feed, id=feed_id)

        if serializer.is_valid():
            feed.report_point += 1
            feed.save()
            serializer.save(user=request.user, feed_id=feed_id)
            
        return Response({"message":"신고가 완료되었습니다."}, status=status.HTTP_200_OK)
    

# 검색어 전체 조회 View
class CommunitySearchWordListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    # 검색어 조회
    def get(self, request):
        words = SearchWord.objects.all().order_by('-created_at')
        serializer = SearchWordSerializer(words, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

# 검색어 랭킹 View
class SearchWordRankingView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    # 검색어 랭킹 조회
    def get(self, requset):
        words = SearchWord.objects.all().order_by('word')
        serializer = SearchWordSerializer(words, many=True)
        
        result_set = set()
        word_list = []
        
        for word in serializer.data:
            result_set.add(word['word'])
            
        result_set = list(result_set)
        
        for result in result_set:
            count = 0
            for i in serializer.data:
                i = i['word']
                if result == i:
                    count += 1
            word_list.append({
                "word" : result,
                "count" : count
            })
        
        return Response(word_list, status=status.HTTP_200_OK)
    
class FeedViewSet(ModelViewSet):
    queryset = Feed.objects.none()
    serializer_class = FeedSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['post', ]

    def create(self, request, *args, **kwargs):
        print(viewers_id_list)
        viewers_id_list = [1, 2]
        _serializer = self.serializer_class(data=request.data)
        if _serializer.is_valid():
            _serializer.save(viewers=viewers_id_list)
            return Response(data=_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=_serializer.errors, status=status.HTTP_400_BAD_REQUEST)