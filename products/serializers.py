from rest_framework import serializers
from products.models import Brand, Product, Category


class ProductSerializer(serializers.ModelSerializer): # 상품 정보 전체 조회,
    
    class Meta:
        model = Product
        fields = '__all__'
        

class BrandSerializer(serializers.ModelSerializer): # 브랜드 정보 전체 조회,
    
    class Meta:
        model = Brand
        fields = '__all__'
        

class CategorySerializer(serializers.ModelSerializer): # 카테고리 정보 전체 조회,
    
    class Meta:
        model = Category
        fields = '__all__'