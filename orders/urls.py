from django.urls import  path
from .views import order_list,checkout,add_to_cart
from .api import OrderListApi,OrderDetail
 

urlpatterns = [
    path('',order_list),
    path('checkout/',checkout),
    path('add-to-cart',add_to_cart),
       
    #Api
    path('api/<str:username>/list',OrderListApi.as_view()),
    path('api/<int:pk>',OrderDetail.as_view()),
       
]