from rest_framework import serializers
from products.models import Product
from weather.models import Weather

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields='__all__'

class RegionSerializer(serializers.ModelSerializer):


    class Meta:
        model = Weather
        fields = ('city',)