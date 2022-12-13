from rest_framework import serializers
from products.models import Product
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)     
from communities.models import Feed,Comment,ReComment,ReportFeed, SearchWord


#게시글 작성, 수정 serializer
class FeedSerializer(TaggitSerializer, serializers.ModelSerializer): 
    user = serializers.SerializerMethodField()
    tags = TagListSerializerField()
        
    def get_user(self, obj):
        return obj.user.email    

    def validate(self, data):
        tags = data['tags']
        return data

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        validated_data.pop('like')
        validated_data.pop('unlike')
        instance = Feed.objects.create(**validated_data)
        for tag in tags:
            tag = tag.strip().split('#')
            for feed_tag in tag:                
                if feed_tag != '':
                    instance.tags.add(feed_tag.strip())
        return instance
                
    class Meta:
        model = Feed
        fields = '__all__'

        
# 게시글 전체 보기 serializer
class FeedListSerializer(TaggitSerializer, serializers.ModelSerializer): 
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

    def get_user_id(self, obj):
        return obj.user.user_id
    class Meta:
        model = Feed
        fields = '__all__'


#  대댓글을 작성을 위한 Serializer
class ReCommentListSerializer(serializers.ModelSerializer):
   
    user = serializers.SerializerMethodField()
    
    def get_user(self, obj):
        return obj.user.nickname

    class Meta:
        model = ReComment
        fields='__all__'
        
#  대댓글을 보기위한 Serializer
class ReCommentListSerializer(serializers.ModelSerializer):
    
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

# 게시글 댓글을 보기 작성 Serializer
class CommentListViewSerializer(serializers.ModelSerializer):
    
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

# 게시글 댓글을 작성을 위한 Serializer
    
class CommentListSerializer(serializers.ModelSerializer):
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
        
#게시글 상세보기serializer
class FeedDetailSerializer(TaggitSerializer, serializers.ModelSerializer): 
    
    user = serializers.SerializerMethodField()
    comments = CommentListViewSerializer(source = "feeds", many=True)
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


# 상품 검색 serializer
class SearchProductSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Product
        fields = '__all__'

#신고 serializer       
class ReportSerializer(serializers.ModelSerializer): 

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
        