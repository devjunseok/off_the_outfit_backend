from rest_framework import serializers
from products.models import Product
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)        #태그
from communities.models import Feed,Comment,ReComment,ReportFeed


class FeedSerializer(TaggitSerializer, serializers.ModelSerializer): #게시글 작성, 수정 시리얼라이즈
    user = serializers.SerializerMethodField()
    tags = TagListSerializerField()

    
    def get_user(self, obj):
        return obj.user.email
    
    
    class Meta:
        model = Feed
        fields = '__all__'
        

class FeedListSerializer(TaggitSerializer, serializers.ModelSerializer): # 게시글 전체 보기 serializer
    tags = TagListSerializerField()
    like_count = serializers.SerializerMethodField()
    
    def get_like_count(self, obj):  
        return obj.like.count()

    class Meta:
        model = Feed
        fields = '__all__'


class ReCommentListSerializer(serializers.ModelSerializer): #  대댓글을 작성을 위한 Serializer
    
    user = serializers.SerializerMethodField()
    


    def get_user(self, obj):
        return obj.user.nickname

    class Meta:
        model = ReComment
        fields='__all__'
        
class ReCommentListSerializer(serializers.ModelSerializer): #  대댓글을 보기위한 Serializer
    
    user = serializers.SerializerMethodField()
    


    def get_user(self, obj):
        return obj.user.nickname

    class Meta:
        model = ReComment
        fields='__all__'
        
class CommentListViewSerializer(serializers.ModelSerializer): # 게시글 댓글을 보기 작성 Serializer
    
    user = serializers.SerializerMethodField()
    recomment = ReCommentListSerializer(source = "comments", many=True)

    
    def get_user(self, obj):
        return obj.user.nickname
    
    class Meta:
        model = Comment
        fields = '__all__'

class CommentListSerializer(serializers.ModelSerializer): # 게시글 댓글을 작성을 위한 Serializer
    
    user = serializers.SerializerMethodField()
    

    def get_user(self, obj):
        return obj.user.nickname

    class Meta:
        model = Comment
        fields='__all__'
        

class FeedDetailSerializer(TaggitSerializer, serializers.ModelSerializer): #게시글 상세보기serializer
    
    user = serializers.SerializerMethodField()
    comments = CommentListViewSerializer(source = "feeds", many=True) # 게시글관련 댓글 보기위한 Serializer 설정
    tags = TagListSerializerField()
    like_count = serializers.SerializerMethodField()
    
    

    def get_user(self, obj):
        return obj.user.nickname
    
    def get_like_count(self, obj):  
        return obj.like.count()
    
    
    class Meta:
        model = Feed
        fields = '__all__'


class SearchProductSerializer(serializers.ModelSerializer): # 상품 검색
    

    class Meta:
        model = Product
        fields = '__all__'
        
class ReportSerializer(serializers.ModelSerializer): #신고 시리얼라이즈
    user = serializers.SerializerMethodField()
    
    def get_user(self, obj):
        return obj.user.email
    
    class Meta:
        model = ReportFeed
        fields = '__all__'
