from django.urls import  path
from .views import order_list,checkout,add_to_cart
from .api import OrderListApi
 

urlpatterns = [
    path('',order_list),
    path('checkout',checkout),
    path('add-to-cart',add_to_cart),
       
    #Api
    path('api/<str:username>/list',OrderListApi.as_view()),
       
]