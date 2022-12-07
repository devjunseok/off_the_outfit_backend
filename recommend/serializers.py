from rest_framework import serializers
from products.models import Product
from weather.models import Weather


class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Weather
        fields = ('city',)