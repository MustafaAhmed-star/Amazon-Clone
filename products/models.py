from django.db import models
from  django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

FLAG_TYPES ={
    ('New','New'),
    ('Sale','Sale'),
    ('Feature','Feature'),

}
class Product(models.Model):
    name = models.CharField(_('name'),max_length=200)
    flag = models.CharField(_('flag'),max_length=20,choices=FLAG_TYPES)
    price = models.FloatField(_('price'),)
    image = models.ImageField(_('image'),upload_to='product')
    sku  = models.IntegerField(_('sku'),)
    subtitle = models.TextField(_('subtitle'),max_length=350)
    description = models.TextField(_('description'),max_length=1000)
    tags = TaggableManager()
    brand  = models.ForeignKey('Brand',verbose_name='brand',related_name='product_brand' ,on_delete=models.SET_NULL,null = True)
    create_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True,null=True)
    class Meta:
        ordering = ('create_at',) 
    
    def __str__(self):
        return self.name
        
    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args,**kwargs)
class ProductImages(models.Model):
    product = models.ForeignKey(Product,related_name='product_image' ,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='productImages')


class Brand(models.Model):
    name = models.CharField(_('name'),max_length=100)
    image=models.ImageField(_('image'),upload_to='brand')
    slug = models.SlugField(blank=True,null=True)
    
    
    def __str__(self):
        return self.name
        
    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super(Brand, self).save(*args,**kwargs)
    
class Review(models.Model):
    user = models.ForeignKey(User,verbose_name='user', on_delete=models.SET_NULL,null = True)
    product = models.ForeignKey(Product,verbose_name='product',related_name='review_product', on_delete=models.CASCADE)
    review = models.TextField(_('review'),max_length=300)
    rate = models.IntegerField(_('rate'),choices=[(i,i) for i in range(1,6)])
    create_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{str(self.user)} review {str(self.product)}'