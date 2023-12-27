from rest_framework import serializers
from .models import Product , Brand ,Review,ProductImages


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ['product']
class ProductImagesSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ['image']
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
        reviews = object.review_product.all()
        
        avg = sum(review.rate for review in reviews) / len(reviews) if len(reviews) > 0 else 0
        return avg
        
class ProductDetailSerializers(serializers.ModelSerializer):
    brand = serializers.StringRelatedField() 
    review_count = serializers.SerializerMethodField()
    avg_rate = serializers.SerializerMethodField()
    images = ProductImagesSerializers(source = 'product_image',many =True)
    reviews = ReviewSerializer(source = 'review_product',many=True)
    class Meta:
        model = Product
        fields= '__all__'
    def get_review_count(self,object):
        return object.review_product.all().count()
    def get_avg_rate(self,object):
        reviews = object.review_product.all()
        avg = sum(review.rate for review in reviews) / len(reviews) if len(reviews) > 0 else 0
        return avg
class BrandListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields= '__all__'
    
class BrandDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields= '__all__'
    