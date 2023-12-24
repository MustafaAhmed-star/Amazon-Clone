from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

 
##################################
from . import serializers
from .models import Product,Brand 
from .pagination import ProductPaginator

class ProductListApi(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductListSerializers
    pagination_class = ProductPaginator
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter] 
    filterset_fields = ['brand', 'flag']
    search_fields = ['name','subtitle','description']
    ordering_fields = ['price', ]
    ordering = ['price'] # if i have more one fields use ordering to make a default
    
class ProductDetailApi(generics.RetrieveAPIView):
    queryset = Product 
    serializer_class = serializers.ProductDetailSerializers
    
    
class BrandListApi(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = serializers.BrandListSerializers
    filter_backends = [filters.SearchFilter] 
    search_fields = ['name']
    
class BrandDetailApi(generics.RetrieveAPIView):
    queryset = Brand 
    serializer_class = serializers.BrandDetailSerializers
 