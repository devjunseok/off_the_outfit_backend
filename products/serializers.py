from rest_framework import serializers
from products.models import Brand, Product, Category, Post, Reply, Closet, NameTag, ProductCategoryRelation

# Category :: 카테고리 정보 관련 Serializer
class CategorySerializer(serializers.ModelSerializer): # 카테고리 정보 전체 조회,
    
    class Meta:
        model = Category
        fields = '__all__'


# Products :: 상품 정보 관련 Serializer 
class ProductSerializer(serializers.ModelSerializer): # 상품 정보 전체 조회,
    brand_name_kr = serializers.SerializerMethodField()
    brand_name_en = serializers.SerializerMethodField()
    category = CategorySerializer(many=True)

    def get_brand_name_kr(self, obj):
        return obj.brand.brand_name_kr
    
    def get_brand_name_en(self, obj):
        return obj.brand.brand_name_en
    
    class Meta:
        model = Product
        fields = ("pk", "category", "brand_name_kr", "brand_name_en", "product_number", "product_name", "product_image", "original_price", "discount_price", "review_count", "brand")
        
        
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
        
        
        
        
# Closet :: 옷장 관련 Serializer
class ClosetSerializer(serializers.ModelSerializer): # 상품 기준 옷장 조회, 등록
    user = serializers.SerializerMethodField()
    
    def get_user(self, obj):
        return obj.user.nickname
    
    class Meta:
        model = Closet
        fields = '__all__'
        

class NameTagSerializer(serializers.ModelSerializer): # 유저 옷장 태그 등록
    user = serializers.SerializerMethodField()

    
    def get_user(self, obj):
        return obj.user.nickname
    
    class Meta:
        model = NameTag
        fields = '__all__'
        


class NameTagViewSerializer(serializers.ModelSerializer): # 유저 옷장 태그 조회
    user = serializers.SerializerMethodField()
    closet = ClosetSerializer(source = "nametags", many=True)

    def get_user(self, obj):
        return obj.user.nickname

    class Meta:
        model = NameTag
        fields = '__all__'