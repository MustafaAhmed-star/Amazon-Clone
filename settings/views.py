from django.shortcuts import render
from django.db.models import Count
from products.models import Product,Brand,Review
def home(request):
    new_product = Product.objects.filter(flag='New')[:10]
    sale_product = Product.objects.filter(flag='Sale')[:10]
    feature_product = Product.objects.filter(flag='Feature')[:6]
    brands = Brand.objects.annotate(product_count = Count('product_brand'))
    reviews = Review.objects.all()[:6]
    context = {
    'new_product':new_product,
    'sale_product':sale_product,
    'feature_product':feature_product,
    'brands':brands,
    'reviews':reviews,
 }

    return render(request,'settings/home.html',context)