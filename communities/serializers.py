from rest_framework import serializers
from products.models import Product
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)        #태그
from communities.models import Feed,Comment,ReComment,ReportFeed, SearchWord


class FeedSerializer(TaggitSerializer, serializers.ModelSerializer): #게시글 작성, 수정 시리얼라이즈
    user = serializers.SerializerMethodField()
    tags = TagListSerializerField()

    
    def get_user(self, obj):
        return obj.user.email
    
    
    class Meta:
        model = Feed
        fields = '__all__'
        

class FeedListSerializer(TaggitSerializer, serializers.ModelSerializer): # 게시글 전체 보기 serializer
    user = serializers.SerializerMethodField()
    tags = TagListSerializerField()
    like_count = serializers.SerializerMethodField()
    unlike_count = serializers.SerializerMethodField()
    reports = serializers.SerializerMethodField()
    
    def get_reports(self, instance):
        reports = instance.reports.all()
        return ReportSerializer(reports, many=True).data
    
    def get_user(self, obj):
        return obj.user.nickname
    
    def get_like_count(self, obj):  
        return obj.like.count()
    
    def get_unlike_count(self, obj):  
        return obj.unlike.count()

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
    profile_image = serializers.SerializerMethodField()
    
    def get_user(self, obj):
        return obj.user.nickname
    
    def get_user_id(self, obj):
        return obj.user.user_id
    
    def get_profile_image(self, obj):
        return obj.user.profile_image.url

    class Meta:
        model = ReComment
        fields=("pk", "user_id", "user", "recomment", "comment", "profile_image", "recomment_like", "created_at")
        
class CommentListViewSerializer(serializers.ModelSerializer): # 게시글 댓글을 보기 작성 Serializer
    
    user = serializers.SerializerMethodField()
    recomment = ReCommentListSerializer(source = "comments", many=True)
    profile_image = serializers.SerializerMethodField()

    
    def get_user(self, obj):
        return obj.user.nickname

    def get_user_id(self, obj):
        return obj.user.user_id
    
    def get_profile_image(self, obj):
        return obj.user.profile_image.url

    class Meta:
        model = Comment
        fields = ("pk", "user_id", "user", "recomment", "comment", "profile_image", "comment_like", "created_at", "updated_at", "feed")

class CommentListSerializer(serializers.ModelSerializer): # 게시글 댓글을 작성을 위한 Serializer
    
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.nickname
    
    def get_user_id(self, obj):
        return obj.user.user_id
    
    def get_profile_image(self, obj):
        return obj.user.profile_image.url

    class Meta:
        model = Comment
        fields='__all__'
        

class FeedDetailSerializer(TaggitSerializer, serializers.ModelSerializer): #게시글 상세보기serializer
    
    user = serializers.SerializerMethodField()
    comments = CommentListViewSerializer(source = "feeds", many=True) # 게시글관련 댓글 보기위한 Serializer 설정
    profile_image = serializers.SerializerMethodField()
    tags = TagListSerializerField()
    like_count = serializers.SerializerMethodField()
    
    def get_user(self, obj):
        return obj.user.nickname
    
    def get_like_count(self, obj):  
        return obj.like.count()
    
    def get_user_id(self, obj):
        return obj.user.user_id
    
    def get_profile_image(self, obj):
        return obj.user.profile_image.url
    
    class Meta:
        model = Feed
        fields = ("pk", "user_id", "user", "comments", "profile_image", "tags", "like_count", "content", "image", "created_at", "updated_at", "report_point", "like", "unlike")


class SearchProductSerializer(serializers.ModelSerializer): # 상품 검색
    

    class Meta:
        model = Product
        fields = '__all__'
        
class ReportSerializer(serializers.ModelSerializer): #신고 시리얼라이즈

    user = serializers.SerializerMethodField()
    

    def get_user(self, obj):
        return obj.user.nickname

    class Meta:
        model = ReportFeed
        fields='__all__'
        

# SearchWord :: 검색어 관련 Serializer
class SearchWordSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SearchWord
        fields = '__all__'
        