from rest_framework import serializers
from communities.models import Feed
from products.models import Products
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)        #태그

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


class FeedDetailSerializer(serializers.ModelSerializer): #게시글 상세보기 serializer
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.nickname
    
    class Meta:
        model = Feed
        fields = '__all__'

class SearchProductSerializer(serializers.ModelSerializer): # 상품 검색
    

    class Meta:
        model = Products
        fields = '__all__'