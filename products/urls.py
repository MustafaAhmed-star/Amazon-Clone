from django.urls import  path
from . import views



urlpatterns = [
    path('brands/',views.BrandList.as_view()),
    path('brands/<slug:slug>/',views.BrandDetail.as_view()),
    path('',views.ProductList.as_view()),
    # path('<int:pk>/',views.ProductList.as_view()),
    path('<slug:slug>/',views.ProductDetail.as_view()),
    
]