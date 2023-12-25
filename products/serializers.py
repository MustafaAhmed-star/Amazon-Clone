from rest_framework import serializers
from .models import Product , Brand ,Review



class ProductListSerializers(serializers.ModelSerializer):
    brand = serializers.StringRelatedField() 
    review_count = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields= '__all__'
    def get_review_count(self,object):
        return object.review_product.all().count()
class ProductDetailSerializers(serializers.ModelSerializer):
    brand = serializers.StringRelatedField() 
    review_count = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields= '__all__'
    def get_review_count(self,object):
        return object.review_product.all().count()

class BrandListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields= '__all__'
    
class BrandDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields= '__all__'
    