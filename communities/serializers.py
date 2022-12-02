from rest_framework import serializers
from communities.models import Feed,Comment

class FeedSerializer(serializers.ModelSerializer): #게시글 작성, 수정 시리얼라이즈
    user = serializers.SerializerMethodField()
    
    def get_user(self, obj):
        return obj.user.email
    
    class Meta:
        model = Feed
        fields = '__all__'
        

class FeedListSerializer(serializers.ModelSerializer): # 게시글 전체 보기 serializer

    class Meta:
        model = Feed
        fields = '__all__'



class CommentListSerializer(serializers.ModelSerializer): # 게시글 댓글을 보기위한 Serializer
    
    user = serializers.SerializerMethodField()
  
  
    def get_user(self, obj):
          return obj.user.nickname

    class Meta:
        model = Comment
        fields='__all__'
        
class FeedDetailSerializer(serializers.ModelSerializer): #게시글 상세보기 serializer
    
    user = serializers.SerializerMethodField()
  
  
    def get_user(self, obj):
        return obj.user.nickname
    class Meta:
        model = Feed
        fields = '__all__'
