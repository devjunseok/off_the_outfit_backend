from rest_framework import serializers
from communities.models import Feed


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
