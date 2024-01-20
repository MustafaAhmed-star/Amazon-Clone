from django.shortcuts import render
from django.views import generic
from .models import Product,Review,ProductImages,Brand 
from django.db.models import Count


from django.views.decorators.cache import cache_page


@cache_page(30)
def debug(request):
    # data = Product.objects.select_related('brand').all()
    # data =  Product.objects.filter(price__gt= 20)
    # data =  Product.objects.filter(price__lte= 40)
    # data =  Product.objects.filter(price__range=(70,90))
    # data =  Product.objects.filter(brand___name='apple')
    # data =  Product.objects.filter(brand__price__gt=30)
    # data = Product.objects.filter(name__startswith='Kathy')
    # data = Product.objects.filter(name__endswith='Kathy')
    # data = Product.objects.filter(name__endswith='Mack')
    # data = Product.objects.filter(tags__isnull=True)
    # data = Review.objects.filter(created_at__year = 2023)
    # data = Product.objects.filter(price__gt=80 , quantity__lt=20)
    # data = Product.objects.filter(Q(price__gt=80) | Q(quantity__lt=20))
    # data = Product.objects.filter(~Q(price__gt=80) |Q(quantity__lt=20))
    # data = Product.objects.filter(price = F('quantity'))
    # data = Product.objects.all().order_by('name')
    # data = Product.objects.all().order_by('-name')
    # data = Product.objects.all()[10:40]
    # data = Product.objects.values('name','price','brand__name')
    # data = Product.objects.values('name','price')
    # data = Product.objects.defer('slug','discription')
    # data = Product.objects.values_list('name','price')
    # data = Product.objects.aaggregate(Sum='quantaity')
    # data = Product.objects.aaggregate(Avg=Price)
    # data = Product.objects.annotate(price_with_tax=F('price')*1.5)
    data = Product.objects.all()
    return render(request, 'products/debug.html', {'data':data})


class ProductList(generic.ListView):
    model = Product
    paginate_by = 25
    
class ProductDetail(generic.DetailView):
    model = Product
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["reviews"] = Review.objects.filter(product =self.get_object())
        context["images"] =  ProductImages.objects.filter(product =self.get_object())
        context["related"] =  Product.objects.filter(brand =self.get_object().brand)[:5]
        return context        
        
        
class BrandList(generic.ListView):
    model = Brand
    paginate_by = 25
    queryset = Brand.objects.annotate(products_count =Count('product_brand'))

class BrandDetail(generic.ListView):
    model = Product
    template_name = 'products/brand_detail.html'
    paginate_by = 25

    def get_queryset(self):
        brand  = Brand.objects.get(slug = self.kwargs['slug'])
        queryset = super().get_queryset().filter(brand=brand)
        return queryset
        
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context["brand"] = Brand.objects.filter(slug = self.kwargs['slug']).annotate(products_count =Count('product_brand'))[0]
        return context
    
        
    