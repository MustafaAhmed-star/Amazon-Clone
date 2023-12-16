from django.shortcuts import render
from django.views import generic
from . import models

class ProductList(generic.ListView):
    model = models.Product
    
class ProductDetail(generic.DetailView):
    model = models.Product
