from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from products.models import Product
import datetime





    
    
class Coupon(models.Model):
    code = models.CharField(max_legnth = 25)
    quatity = models.IntegerField()
    discount = models.IntegerField()
    start_date = models.DateTimeField(default = timezone.now)
    end_date = models.DateTimeField(null = True,blank = True)
    
    def save(self,*args,**kwargs):
       week = datetime.timedelta(days=7)
       self.end_date = self.start_date + week       
       super(Coupon, self).save(*args, **kwargs)