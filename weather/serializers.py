from rest_framework import serializers
from weather.models import Weather

# 날씨 정보 조회 serializer
class WeatherSerializer(serializers.ModelSerializer): 
    
    class Meta:
        model = Weather
        fields = '__all__'
        
        

