from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from utils.generate_code import generate_code
# Create your models here.


PHONE_TYPE = (("Primary","Primary"),('Secondary','Secondary'),)

class Profile(models.Model):
    user = models.OneToOneField(User,related_name = 'profile' ,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile')
    code = models.CharField(max_length=50,default = generate_code)
    
    def __str__(self):
        return str(self.user)
@receiver(post_save,sender=User)
def createProfile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(
            user = instance,
            
        
        )
class NumberContact(models.Model):
    user = models.ForeignKey(User,related_name = 'user_contacts' ,on_delete=models.CASCADE)
    type = models.CharField(max_length = 11,choices = PHONE_TYPE)
    number = models.CharField( max_length=50)

ADDRESS_TYPE =(
    ('Home','Home'),
    ('Office','Office'),
    ('Bussines','Bussines'),
    ('Other','Other'),

)
class Adress(models.Model):
    user =models.ForeignKey(User,on_delete =models.CASCADE)
    address= models.TextField(max_length=150)
    type = models.CharField(max_length= 15 ,choices = ADDRESS_TYPE)
    
    def __str__(self) -> str:
        return self.address