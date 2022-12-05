from rest_framework import serializers
from weather.models import Weather

# Products :: 상품 정보 관련 Serializer 
class WeatherSerializer(serializers.ModelSerializer): # 날씨 정보 전체 조회,
    
    class Meta:
        model = Weather
        fields = '__all__'
        
        

