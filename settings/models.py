from django.db import models

# Create your models here.



class Settings(models.Model):
    name = models.CharField(max_length=60)
    logo = models.ImageField(upload_to='settings')
    subtitle = models.TextField(max_length=100)
    email_us = models.CharField(max_length=100,null=True,blank=True)
    call_us = models.TextField(max_length=100,null=True,blank=True)
    email = models.TextField(max_length=100,null=True,blank=True)
    phones= models.TextField(max_length=100,null=True,blank=True)
    address = models.TextField(max_length=100,null=True,blank=True)
    twiter_link =  models.URLField(null=True,blank=True, max_length=200)
    youtube_link =  models.URLField(null=True,blank=True, max_length=200)
    facebook_link = models.URLField(null=True,blank=True, max_length=200)
    android_app = models.URLField(null=True,blank=True, max_length=200)
    ios_app = models.URLField(null=True,blank=True, max_length=200)
    android_app = models.URLField(max_length=100,null=True,blank=True)
 




    def __str__(self):

        return self.name
    
 