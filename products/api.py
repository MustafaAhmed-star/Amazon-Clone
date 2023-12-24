from rest_framework import generics
from . import serializers
from .models import Product,Brand 
from .pagination import ProductPaginator

class ProductListApi(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductListSerializers
    pagination_class = ProductPaginator
    
    
class ProductDetailApi(generics.RetrieveAPIView):
    queryset = Product 
    serializer_class = serializers.ProductDetailSerializers
    
    
class BrandListApi(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = serializers.BrandListSerializers
    
    
class BrandDetailApi(generics.RetrieveAPIView):
    queryset = Brand 
    serializer_class = serializers.BrandDetailSerializers
 