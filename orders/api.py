from rest_framework import generics
from django.contrib.auth.models import User
from django.shortcuts import  get_object_or_404
from rest_framework.response import Response
import datetime
from rest_framework import status 

from .models import Order,OrderItems,Cart,CartItems,Coupon
from .serializers import  OrderSerializer, OrderItemSerializer, CartSerializer,CartItemSerializer
from settings.models import DeliveryFee
from products.models import Product
from accounts.models import Adress


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
                return Response({'message':'coupon was applied successfully'},status=status.HTTP_200_OK)
            else:
                return Response({'message':'coupon was invalid or expired'},status = status.HTTP_204_NO_CONTENT)
        return Response({'message':'coupon is not found '},status=status.HTTP_404_NOT_FOUND)
        
        
class OrderCreateApi(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        user =User.objects.get(username = self.kwargs["username"])
        code = request.data["payment_code"]
        address = request.data["address_id"]
        
        cart = Cart.objects.get(user = user , status = 'InProgress')
        cartItems = CartItems.objects.filter(cart = cart)
        user_address = Adress.objects.get(id = address)
        
        
        #cart : order  , cartItems : orderItems
        new_order = Order.objects.create(
            user = user,
            status = 'Recieved',
            code = code , 
            delivery_location = user_address,
            coupon = cart.coupon,
            total_after_coupen=cart.total_after_coupon,
            total = cart.cart_total
        )
        #orderItems
        for item in cartItems:
            OrderItems.objects.create(
                order = new_order,
                product = item.product,
                price = item.product.price,
                quantity = item.quantity,
                total  = item.total,
            
            )
            #decrease product quantity
            item.product.quantity -= item.quantity
            item.save()
        #close the cart 
        
        cart.status = 'Completed'
        cart.save()
        #send email
        return Response({"message":"Order Created Successfully"},status= status.HTTP_201_CREATED)
class CartCUDApi(generics.GenericAPIView):
    def get(self,request,*args, **kwargs):
        # get or create
        user = User.objects.get(username = self.kwargs['username'])
        cart = Cart.objects.get_or_create(user = user , status = 'InProgress')
        serializers = CartSerializer(cart)
        return Response({serializers.data},status = status.HTTP_200_OK)
        
        
    def post(self,request,*args, **kwargs):
        #add or update
        user  = User.objects.get(username = self.kwargs['username'])
        product = Product.objects.get(id = request.data['product_id'])
        quantity = int(request.data['quantity'])
        
        cart  = Cart.objects.get(user = user , status = 'InProgress')
        cartItems,created = CartItems.objects.get_or_create(cart = cart, product = product)
        
        #update
        if not created:
            cartItems.quantity += quantity
            cartItems.save()
            return Response({'message':'cart was updated successfully'},status = status.HTTP_200_OK)
        cartItems.quantity = quantity
        cartItems.save()
        return Response({'message':'cart was updated successfully'},status = status.HTTP_200_OK)
    def delete(self, request, *args, **kwargs):
        #adding error handling to delete func
        try:
            user = User.objects.get(username=self.kwargs['username'])
            product = CartItems.objects.get(id=request.data['item_id'])
            product.delete()
            return Response({'message': 'Item was deleted successfully'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except CartItems.DoesNotExist:
            return Response({'message': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)
