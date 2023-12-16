from django.urls import  path
from . import views



urlpatterns = [
    path('',views.ProductList.as_view()),
    # path('<int:pk>/',views.ProductList.as_view()),
    path('<slug:slug>/',views.ProductList.as_view()),
    
]