from rest_framework import serializers
from products.models import Brand, Products


class ProductsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Products
        fields = '__all__'