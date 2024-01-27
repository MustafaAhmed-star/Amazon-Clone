from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from utils.generate_code  import generate_code
from products.models import Product
from accounts.models import Adress
import datetime


    
ORDER_STATUS = (
    ('Recieved','Recieved'),
    ('Processed','Processed'),
    ('Shipped','Shipped'),
    ('Delivered','Delivered'),
)
CART_STATUS = (
    ('InProgress','InProgress'),  
    ('Completed','Completed')
)
class Order(models.Model):
    user =  models.ForeignKey(User,related_name='order_user',on_delete=models.SET_NULL,null=True,blank=True)
    status = models.CharField( max_length=50,choices=ORDER_STATUS,default='Recieved')
    code = models.CharField(max_length=100,null = True , blank = True)
    order_time = models.DateTimeField(default=timezone.now)
    delivery_time = models.DateTimeField(null=True,blank=True)
    delivery_location = models.ForeignKey(Adress,related_name = 'order_address',on_delete=models.CASCADE)
    coupon = models.ForeignKey('Coupon', related_name='order_coupon' ,on_delete=models.SET_NULL,null=True,blank=True)
    total_after_coupen= models.CharField(max_length=100,null=True,blank=True)
    
    def __str__(self):
        return f'order {self.id} for  {str(self.user)}'
    
    
    
    def save(self,*args,**kwargs):
       self.code = generate_code()   
       super(Order, self).save(*args, **kwargs)
    
class OrderItems(models.Model):
    order = models.ForeignKey(Order,related_name='order_detail',on_delete=models.CASCADE)
    product = models.ForeignKey(Product,related_name='order_product',on_delete=models.SET_NULL,null=True,blank=True)
    price = models.FloatField()
    quantity = models.IntegerField(default = 1)
    total = models.FloatField(null=True,blank=True)
 
class Cart(models.Model):
    user =  models.ForeignKey(User,related_name='cart_user',on_delete=models.SET_NULL,null=True,blank=True)
    status = models.CharField( max_length=50,choices=CART_STATUS)
    coupon = models.ForeignKey('Coupon', related_name='cart_coupon' ,on_delete=models.SET_NULL,null=True,blank=True)
    total_after_coupon= models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return str(self.user)
    
    @property
    def cart_total(self):
        return 1

class CartItems(models.Model):
   cart = models.ForeignKey(Cart,related_name='cart_items',on_delete=models.CASCADE)
   product = models.ForeignKey(Product,related_name='cart_product',on_delete=models.SET_NULL,null=True,blank=True)
   quantity = models.IntegerField(default=1)
   total = models.FloatField(null=True,blank=True)

   def __str__(self):
        return str(self.cart)

    
    
class Coupon(models.Model):
    code = models.CharField(max_length = 25)
    quatity = models.IntegerField()
    discount = models.IntegerField()
    start_date = models.DateTimeField(default = timezone.now)
    end_date = models.DateTimeField(null = True,blank = True)
    
    def save(self,*args,**kwargs):
       week = datetime.timedelta(days=7)
       self.end_date = self.start_date + week       
       super(Coupon, self).save(*args, **kwargs)