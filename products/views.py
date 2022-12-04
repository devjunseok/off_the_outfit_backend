from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import pandas as pd
from products.serializers import ProductsSerializer, BrandSerializer, CategorySerializer
from rest_framework import status, permissions
from products.models import Brand, Category, Products
from products.crawling import ProductsUpdate


# Products :: 상품 정보 관련 View 
class ProductInfoUdateView(APIView):
    
    def post(self, request): # 무신사 상품 정보 업데이트 (Crawling)
        category_list = Category.objects.all().values()
        brand_list = Brand.objects.all().values()
        ProductsUpdate(category_list, brand_list)
        return Response({"message":"상품 정보가 등록 되었습니다!"}, status=status.HTTP_200_OK)
    
            
class ProductInfoView(APIView):
    
    def get(self, request): # 상품 정보 전체 조회
        articles = Products.objects.all()
        serializer = ProductsSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request): # 상품 정보 개별 등록
        pass


class ProductInfoDetailView(APIView):
    
    def get(self, request): # 상품 정보 상세 조회
        pass
    
    def put(self, request): # 상품 정보 수정
        pass
    
    def delete(self, request): # 상품 정보 삭제
        pass

class ProductReviewBoardView(APIView):
    
    def get(self, request): # 상품 리뷰 전체 조회
        pass
    
    def post(self, request): # 상품 리뷰 작성
        pass
    

class ProductReviewDetailView(APIView):
    
    def get(self, request): # 상품 리뷰 상세 조회
        pass
    
    def put(self, request): # 상품 리뷰 수정
        pass
    
    def delete(self, request): # 상품 리뷰 삭제
        pass
    

class ProductReviewReplyView(APIView):
    
    def get(self, request): # 상품 리뷰 댓글 전체 조회
        pass
    
    def post(self, request): # 상품 리뷰 댓글 등록
        pass

class ProductReviewReplyDetailView(APIView):

    def delete(self, request): # 상품 리뷰 댓글 삭제
        pass


# Brand :: 브랜드 정보 관련 View 
class BrandInfoUpdateView(APIView):
    
    def post(self, request): # 브랜드 정보 업데이트 (CSV)
        data = pd.read_csv('products/csv/brand_info.csv')

        for br in data['info']:
            brand = Brand()
            br_kr, br_en, br_link = br.split('|')
            
            # 중복 체크
            try : # 중복 브랜드
                brand_double_check = Brand.objects.get(brand_link=br_link)
            except : # 신규 브랜드
                brand_double_check = None
            
            if brand_double_check == None:
                brand.brand_name_kr = br_kr
                brand.brand_name_en = br_en
                brand.brand_link = br_link
                brand.save()
        
        return Response({"message":"브랜드 정보가 등록 되었습니다!"}, status=status.HTTP_200_OK)
    

class BrandInfoView(APIView):
    
    def get(self, request): # 브랜드 정보 전체 조회
        articles = Brand.objects.all()
        serializer = BrandSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request): # 브랜드 정보 개별 등록
        pass


# Category :: 카테고리 정보 관련 View     
class CategoryInfoUpdateView(APIView):
    
    def post(self, request): # 카테고리 정보 업데이트 (CSV)
        data = pd.read_csv('products/csv/category_info.csv')
        
        for cate in data['info']:
            category = Category()
            main_number, main_kr, main_en, sub_number, sub_kr, link = cate.split('|')
            
            # 중복 체크
            try : # 중복 카테고리
                category_double_check = Category.objects.get(category_link=link)
            except : # 신규 카테고리
                category_double_check = None
            
            if category_double_check == None:
                category.main_category_number = main_number
                category.main_category_name = main_kr
                category.sub_category_number = sub_number
                category.sub_category_name = sub_kr
                category.category_link = link
                category.save()
        
        return Response({"message":"카테고리 정보가 등록 되었습니다!"}, status=status.HTTP_200_OK)


class CategoryInfoView(APIView):
    
    def get(self, request): # 카테고리 정보 전체 조회
        articles = Category.objects.all()
        serializer = CategorySerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)