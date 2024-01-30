from rest_framework import serializers
from .models import Order,OrderItems,Cart,CartItems,Coupon

class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields ='__all__'
        
        
class OrderSerializer(serializers.ModelSerializer):
    orderItems = OrderItemsSerializer(many = True)
    class Meta:
        model = Order
        fields ='__all__'
        
        
class CartItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItems
        fields = '__all__'
        
        
class CartSerializer(serializers.ModelSerializer):
    cartItems = CartItemsSerializer(many=True)
    class Meta:
        model = Cart
        fields = '__all__'
        