from rest_framework import serializers
from products.models import Brand, Product, Category, Post, Reply, Closet, NameTag


# Products :: 상품 정보 관련 Serializer 
class ProductSerializer(serializers.ModelSerializer): # 상품 정보 전체 조회,
    
    class Meta:
        model = Product
        fields = '__all__'
        

class ProductDetailSerializer(serializers.ModelSerializer): # 상품 정보 상세 조회,
    
    class Meta:
        model = Product
        fields = '__all__'  
        

class PostSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    
    def get_user(self, obj):
        return obj.user.nickname
    
    class Meta:
        model = Post
        fields = '__all__'
        
  
class ReplySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    
    def get_user(self, obj):
        return obj.user.nickname
    
    class Meta:
        model = Reply
        fields = '__all__'        


# Brand :: 브랜드 정보 관련 Serializer
class BrandSerializer(serializers.ModelSerializer): # 브랜드 정보 전체 조회,
    
    class Meta:
        model = Brand
        fields = '__all__'
        
        
# Category :: 카테고리 정보 관련 Serializer
class CategorySerializer(serializers.ModelSerializer): # 카테고리 정보 전체 조회,
    
    class Meta:
        model = Category
        fields = '__all__'
        
        
# Closet :: 옷장 관련 Serializer
class ClosetSerializer(serializers.ModelSerializer): # 상품 기준 옷장 조회, 등록
    user = serializers.SerializerMethodField()
    
    def get_user(self, obj):
        return obj.user.nickname
    
    class Meta:
        model = Closet
        fields = '__all__'
        

class NameTagSerializer(serializers.ModelSerializer): # 유저 옷장 태그 조회
    user = serializers.SerializerMethodField()
    closet = ClosetSerializer(source = "nametags", many=True)
    
    def get_user(self, obj):
        return obj.user.nickname
    
    class Meta:
        model = NameTag
        fields = '__all__'