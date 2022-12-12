from weather.models import Weather
from weather.serializers import WeatherSerializer
from weather.crawling import forecast

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import status, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

# 네이버 날씨 크롤링 API View
class WeatherInfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
     # 날씨 정보 전체 조회
    def get(self, request): 

        forecast()
        weather = Weather.objects.all()
        serializer = WeatherSerializer(weather, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)