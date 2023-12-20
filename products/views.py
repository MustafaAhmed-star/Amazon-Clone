from django.shortcuts import render
from django.views import generic
from . import models

class ProductList(generic.ListView):
    model = models.Product
    
class ProductDetail(generic.DetailView):
    model = models.Product
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["reviews"] = models.Review.objects.filter(product =self.get_object())
        return context        