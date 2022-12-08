from rest_framework import serializers
from weather.models import Weather

# 날씨 정보 전체 조회,
class WeatherSerializer(serializers.ModelSerializer): 
    
    class Meta:
        model = Weather
        fields = '__all__'
        
        

