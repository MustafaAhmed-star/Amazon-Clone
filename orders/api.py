from rest_framework import generics
from django.contrib.auth.models import User
from django.shortcuts import  get_object_or_404
from rest_framework.response import Response
import datetime

from .models import Order,OrderItems,Cart,CartItems,Coupon
from .serializers import  OrderSerializer, OrderItemSerializer, CartSerializer,CartItemSerializer
from settings.models import DeliveryFee
from products.models import Product



class OrderListApi(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    
    def get_queryset(self):
        queryset = super(OrderListApi, self).get_queryset()
        user = User.objects.get(username = self.kwargs['username'])
        queryset = queryset.filter(user = user)
        return queryset
        
    # def list(self,request,*args, **kwargs):
    #     queryset = super(OrderListApi, self).get_queryset()
    #     user = User.objects.get(username = self.kwargs['username'])
    #     queryset = queryset.filter(user= user) # TODO
    #     data = OrderSerializer(queryset,many = True)
    #     return Response({'orders':data.data})

class OrderDetailApi(generics.RetrieveAPIView):
    queryset = Order
    serializer_class = OrderSerializer
    
class ApplyCoupon(generics.GenericAPIView):
    
    def post(self, request, *args, **kwargs):
        user =User.objects.get(username = self.kwargs["username"])
        coupon = get_object_or_404(Coupon,code = request.data["coupon_code"])
        deliveryFee = DeliveryFee.objects.last().fee
        cart = Cart.objects.get(user= user , status = "InProgress")
        if coupon and coupon.quantity > 0:
            today_date = datetime.datetime.today().date()
            
            if today_date >= coupon.start_date.date() and today_date <= coupon.end_date.date():
                coupon_value =  cart.cart_total * coupon.discount/100
                subTotal = cart.cart_total - coupon_value
                total = round(subTotal + deliveryFee,2)
                cart.coupon = coupon
                cart.total_after_coupon = subTotal
                cart.save()
                coupon.quantity -=1
                coupon.save()
                return Response({'message':'coupon was applied successfully'})
            else:
                return Response({'message':'coupon was invalid or expired'})
        return Response({'message':'coupon is not found '})