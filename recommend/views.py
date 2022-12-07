from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from recommend.serializers import ProductSerializer
from products.models import Product
from django.db.models import Q

class ProductRecommendView(APIView): 
    
    def get(self, request):
        product = Product.objects.filter(Q(category__gte=19) & Q(category__lte=36))
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)