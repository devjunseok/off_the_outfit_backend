import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import sqlite3
from pprint import pprint
from users.serializers import UserProfileSerializer
from users.models import User
from products.serializers import ProductSerializer
from products.models import Product
from recommend.serializers import ProductSerializer,RegionSerializer
from weather.serializers import WeatherSerializer
from weather.models import Weather
from django.db.models import Q
from datetime import date
import random



class ClosetUserRecommend(APIView):
    
    def get(self, request): 
        #유저 기반 추천
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
        print(recommend_list)
        recommend_list = [x for x in recommend_list.keys()]
        
        users = User.objects.filter(id__in=recommend_list)
        serializer = UserProfileSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

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
        

class ProductRecommendView(APIView): 
    
    def post(self, request):
        # 일자 설정하기
        today = date.today()
        date_year, date_month, date_day= today.year, today.month, today.day
        user_date = date(date_year, date_month, date_day).strftime('%m.%d.')

        # 설정한 일자 + 입력한 지역 정보로 DB에서 온도 출력
        user_day_region = Weather.objects.filter(Q(city=request.data['city']) & Q(day_date = user_date)).values()[0]
        user_temperature = user_day_region['day_temperature']
        
        # 출력한 온도를 기준으로 csv에서 추천 카테고리 출력
        temps_data = pd.read_csv('recommend/csv/temperature.csv')
        find_temps = temps_data.loc[(temps_data['temperature'] == user_temperature)]
        
        # 출력된 카테고리 랜덤으로 아우터, 상의, 하의 각 1개씩 랜덤으로 출력
        r_outer = random.choice(find_temps['outer'].values[0].split(','))
        r_top = random.choice(find_temps['top'].values[0].split(','))
        r_bottom = random.choice(find_temps['bottom'].values[0].split(','))

        # 시연을 위한 프린트문(삭제 예정)
        print(find_temps.iloc[:,1:3])
        print(f"아우터 : {r_outer}")
        print(f"상의 : {r_top}")
        print(f"하의 : {r_bottom}")

        # 온도에 맞는 카테고리 출력 후 해당 카테고리와 일치한 상품 정보에서 '?' 랜덤한 상품 출력
        outer = list(Product.objects.filter(Q(category__sub_category_name=r_outer)).order_by('?'))[0:1]
        top = list(Product.objects.filter(Q(category__sub_category_name=r_top)).order_by('?'))[0:1]
        bottom = list(Product.objects.filter(Q(category__sub_category_name=r_bottom)).order_by('?'))[0:1]
        outer = ProductSerializer(outer, many=True)
        top = ProductSerializer(top, many=True)
        bottom = ProductSerializer(bottom, many=True)
        
        # 출력 양식에 맞춰서 데이터 변환
        serializer = [outer.data[0], top.data[0], bottom.data[0]]
        return Response(serializer, status=status.HTTP_200_OK)
