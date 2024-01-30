from rest_framework import serializers
from .models import Order,OrderItems,Cart,CartItems,Coupon

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields ='__all__'
        
        
class OrderSerializer(serializers.ModelSerializer):
    order_detail = OrderItemSerializer(many = True) # NAME it with same name of related_name 
    class Meta:
        model = Order
        fields ='__all__'
        
        
class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItems
        fields = '__all__'
        
        
class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True) # name it with same name as related_name
    class Meta:
        model = Cart
        fields = '__all__'
        