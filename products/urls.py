from django.urls import  path
from . import views
from .import api


urlpatterns = [
    
    path('brands/',views.BrandList.as_view()),
    path('brands/<slug:slug>/',views.BrandDetail.as_view()),
    path('',views.ProductList.as_view()),
    # path('<int:pk>/',views.ProductList.as_view()),
    path('<slug:slug>/',views.ProductDetail.as_view()),
    
    #api
    path('api/list',api.ProductListApi.as_view()),
    path('api/list/<int:pk>',api.ProductDetailApi.as_view()),
    path('api/brands',api.BrandListApi.as_view()),
    path('api/brands/<int:pk>',api.BrandDetailApi.as_view()),
    
    
]