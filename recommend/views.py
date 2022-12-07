from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from recommend.serializers import ProductSerializer,RegionSerializer
from weather.serializers import WeatherSerializer
from products.models import Product
from weather.models import Weather
from django.db.models import Q
from datetime import datetime

class ProductRecommendView(APIView): 
    
    def post(self, request):
        now_date = datetime.today().strftime("%m.%d.")
        serializer = RegionSerializer(data=request.data)
    
        user_region =  Weather.objects.filter(city=request.data["city"]).values()[1]
        print(user_region)
        user_region=user_region["city"]
        user_day_region = Weather.objects.filter(Q(city=user_region) & Q(day_date = now_date)).values()[0]
        user_temperature = user_day_region["day_temperature"]
        
        if user_temperature < 30:
            if serializer.is_valid():
                print("hi")
                product = Product.objects.filter(Q(category__gte=19) & Q(category__lte=36))
                serializer = ProductSerializer(product, many=True)
                print(serializer)
            return Response(serializer.data)
        return Response("틀렸음")
