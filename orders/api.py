from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.response import Response
from .models import Order,OrderItems,Cart,CartItems
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

class OrderDetail(generics.RetrieveAPIView):
    queryset = Order
    serializer_class = OrderSerializer
    