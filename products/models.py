from django.db import models
from  django.contrib.auth.models import User
from taggit.managers import TaggableManager
FLAG_TYPES ={
    ('New','New'),
    ('Sale','Sale'),
    ('Feature','Feature'),

}
class Product(models.Model):
    name = models.CharField(max_length=200)
    flag = models.CharField(max_length=20,choices=FLAG_TYPES)
    price = models.FloatField()
    image = models.ImageField(upload_to='product')
    sku  = models.IntegerField()
    subtitle = models.TextField(max_length=350)
    description = models.TextField(max_length=1000)
    tags = TaggableManager()
    brand  = models.ForeignKey('Brand',related_name='product_brand' ,on_delete=models.SET_NULL,null = True)
    create_at = models.DateTimeField(auto_now=True)
   
    
    def __str__(self):
        self.name
class ProductImages(models.Model):
    product = models.ForeignKey(Product,related_name='product_image' ,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='productImages')


class Brand(models.Model):
    name = models.CharField(max_length=100)
    image=models.ImageField(upload_to='brand')
    
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null = True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.TextField(max_length=300)
    rate = models.IntegerField(choices=[(i,i) for i in range(1,6)])
    create_at = models.DateTimeField(auto_now=True)
    
    