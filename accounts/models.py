from django.db import models
from django.contrib.auth.models import User
# Create your models here.


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