import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import sqlite3
from users.serializers import UserProfileSerializer
from users.models import User
from products.serializers import ProductSerializer
from products.models import Product
from weather.models import Weather
from django.db.models import Q
from datetime import datetime
from recommend.serializers import RegionSerializer

# 유저 기반 옷장 상품 추천 View
class ClosetUserRecommend(APIView):
    #유저 기반 추천
    def get(self, request): 

        me_id = request.user.id
        closet = sqlite3.connect('./db.sqlite3')
        my_connection = pd.read_sql(f"SELECT id, user_id, product_id FROM closet WHERE user_id = {me_id};", closet, index_col='id')
        connection = pd.read_sql("SELECT id, user_id, product_id FROM closet;", closet, index_col='id')
        closet_merge = pd.merge(connection, my_connection, on='product_id')

        product_user = closet_merge.pivot_table('product_id', index='user_id_x', columns='product_id' )
        product_user = product_user.fillna(0)

        user_collab = cosine_similarity(product_user, product_user)
        user_collab = pd.DataFrame(user_collab, index=product_user.index, columns=product_user.index)

        recommend_list = user_collab[me_id].sort_values(ascending=False)[:10]
        recommend_list = [x for x in recommend_list.keys()]
        
        users = User.objects.filter(id__in=recommend_list)
        serializer = UserProfileSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# 상품 기반 추천 View
class ClosetProductRecommend(APIView):
    
    def get(self, request):
        me_id = request.user.id
        closet = sqlite3.connect('./db.sqlite3')
        my_connection = pd.read_sql(f"SELECT id, user_id, product_id FROM closet WHERE user_id = {me_id};", closet, index_col='id')
        connection = pd.read_sql("SELECT id, user_id, product_id FROM closet;", closet, index_col='id')
        closet_merge = pd.merge(my_connection, connection, on='product_id')
        
        product_user = closet_merge.pivot_table('user_id_y', index='product_id', columns='user_id_y' )
        product_user = product_user.fillna(0)
        print(product_user)
        user_collab = cosine_similarity(product_user, product_user)
        user_collab = pd.DataFrame(user_collab, index=product_user.index, columns=product_user.index)

        recommend_list = user_collab[513].sort_values(ascending=False)[:10]
        print(recommend_list)
        recommend_list = [x for x in recommend_list.keys()]
        
        products = Product.objects.filter(id__in=recommend_list)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
# 날씨 기반 상품 추천 View
class ProductRecommendView(APIView): 
    
    def post(self, request):
        now_date = datetime.today().strftime("%m.%d.")
        serializer = RegionSerializer(data=request.data)
    
        user_region =  Weather.objects.filter(city=request.data["city"]).values()[1]
        user_region=user_region["city"]
        user_day_region = Weather.objects.filter(Q(city=user_region) & Q(day_date = now_date)).values()[0]
        user_temperature = user_day_region["day_temperature"]
        
        if user_temperature < 30:
            if serializer.is_valid():
                product = Product.objects.filter(Q(category__gte=19) & Q(category__lte=36))
                serializer = ProductSerializer(product, many=True)
            return Response(serializer.data)
        return Response({"message":"데이터를 불러올 수 없습니다!"}, status=status.HTTP_400_BAD_REQUEST)