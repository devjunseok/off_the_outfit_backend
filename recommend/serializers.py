from rest_framework import serializers
from products.models import Product
from weather.models import Weather

# 날씨 추천 serializer
class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Weather
        fields = ('city',)