from django.urls import  path
from .views import order_list,checkout,add_to_cart ,payment_success,payment_failed,payment_process
from .api import OrderListApi,OrderDetailApi,ApplyCoupon,CartCUDApi,OrderCreateApi
 

urlpatterns = [
    path('',order_list),
    path('checkout/',checkout),
    path('add-to-cart',add_to_cart),
    path('checkout/payment-process',payment_process),
    path('checkout/payment/success',payment_success),
    path('checkout/payment/failed',payment_failed),
       
    #Api
    path('api/<str:username>/list',OrderListApi.as_view()),
    path('api/<int:pk>',OrderDetailApi.as_view()),
    path('api/<str:username>/apply-coupon',ApplyCoupon.as_view()),
    path('api/<str:username>/order-create',OrderCreateApi.as_view()),
    path('api/<str:username>/cart',CartCUDApi.as_view()),

       
] 