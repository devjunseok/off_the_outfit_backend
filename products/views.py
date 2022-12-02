from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import pandas as pd
from products.serializers import ProductsSerializer
from rest_framework import status, permissions
from products.models import Brand, Category, Products
from products.crawling import ProductsUpdate

# Create your views here.

class ProductsView(APIView):
    def get(self, request):
        articles = Products.objects.all()
        serializer = ProductsSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        category_list = Category.objects.all().values()
        brand_list = Brand.objects.all().values()
        ProductsUpdate(category_list, brand_list)
        return Response({"message":"상품 정보가 등록 되었습니다!"}, status=status.HTTP_200_OK)
        

class BrandInfoUpdate(APIView):
    
    def post(self, request): # 브랜드 정보 업데이트
        data = pd.read_csv('products/csv/brand_info.csv')

        for br in data['info']:
            brand = Brand()
            br_kr, br_en, br_link = br.split('|')
            
            brand.brand_name_kr = br_kr
            brand.brand_name_en = br_en
            brand.brand_link = br_link
            brand.save()
        
        return Response({"message":"브랜드 정보가 등록 되었습니다!"}, status=status.HTTP_200_OK)
    
class CategoryListUpdate(APIView):
    
    def post(self, request):
        data = pd.read_csv('products/csv/category_info.csv')
        
        for cate in data['info']:
            category = Category()
            main_number, main_kr, main_en, sub_number, sub_kr, link = cate.split('|')
            
            category.main_category_number = main_number
            category.main_category_name = main_kr
            category.sub_category_number = sub_number
            category.sub_category_name = sub_kr
            category.category_link = link
            category.save()
        
        return Response({"message":"카테고리 정보가 등록 되었습니다!"}, status=status.HTTP_200_OK)