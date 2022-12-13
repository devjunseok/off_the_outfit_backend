from rest_framework import serializers
from products.models import Brand, Product, Category, Post, Reply, Closet, NameTag, ProductCategoryRelation

# Category :: 카테고리 정보 관련 Serializer
class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = '__all__'


# Products :: 상품 정보 관련 Serializer 
class ProductSerializer(serializers.ModelSerializer): 
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
        
 
 # 상품 정보 게시글 serializer       
class PostSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    
    def get_user(self, obj):
        return obj.user.nickname
    
    class Meta:
        model = Post
        fields = '__all__'
        
# 상품 정보 게시글 댓글 serializer
class ReplySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    
    def get_user(self, obj):
        return obj.user.nickname
    
    class Meta:
        model = Reply
        fields = '__all__'        


# Brand :: 브랜드 정보 관련 Serializer
class BrandSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Brand
        fields = '__all__'
        
        
        
        
# Closet :: 옷장 관련 Serializer
class ClosetSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    
    def get_user(self, obj):
        return obj.user.nickname
    
    class Meta:
        model = Closet
        fields = '__all__'
        
# 유저 기준 옷장 조회 serializer     
class ClosetUserSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    product = ProductSerializer()
    
    def get_user(self, obj):
        return obj.user.nickname
    
    class Meta:
        model = Closet
        fields = ("pk", "user", "product", "name_tag", "created_at", "updated_at")
        

# 유저 옷장 태그 등록 serializer
class NameTagSerializer(serializers.ModelSerializer): 
    user = serializers.SerializerMethodField()

    
    def get_user(self, obj):
        return obj.user.nickname
    
    class Meta:
        model = NameTag
        fields = '__all__'
        

# 유저 옷장 태그 조회 serializer
class NameTagViewSerializer(serializers.ModelSerializer): 
    user = serializers.SerializerMethodField()
    closet = ClosetSerializer(source = "nametags", many=True)

    def get_user(self, obj):
        return obj.user.nickname

    class Meta:
        model = NameTag
        fields = '__all__'