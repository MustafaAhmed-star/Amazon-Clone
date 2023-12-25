from rest_framework import serializers
from .models import Product , Brand ,Review



class ProductListSerializers(serializers.ModelSerializer):
    brand = serializers.StringRelatedField() 
    review_count = serializers.SerializerMethodField()
    avg_rate = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields= '__all__'
    def get_review_count(self,object):
        return object.review_product.all().count()
        
    def get_avg_rate(self,object):
        total = 0
        reviews = object.review_product.all()
        if len(reviews) > 0:
            for item in reviews:
                total+=item
            avg = total/len(reviews)
        else:
            avg = 0.0
        return avg
        
class ProductDetailSerializers(serializers.ModelSerializer):
    brand = serializers.StringRelatedField() 
    review_count = serializers.SerializerMethodField()
    avg_rate = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields= '__all__'
    def get_review_count(self,object):
        return object.review_product.all().count()
    def get_avg_rate(self,object):
        total = 0
        reviews = object.review_product.all()
        if len(reviews) > 0:
            for item in reviews:
                total+=item
            avg = total/len(reviews)
        else:
            avg = 0.0
        return avg
class BrandListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields= '__all__'
    
class BrandDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields= '__all__'
    