from rest_framework import serializers
from .models import Product , Brand



class ProductListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields= '__all__'
    
class ProductDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields= '__all__'
    
class BrandListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields= '__all__'
    
class BrandDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields= '__all__'
    