from django.shortcuts import render,redirect
from .models import Order,Cart,CartItems
from products.models import Product
from settings.models import DeliveryFee

def order_list(request):
    orders = Order.objects.filter(user = request.user)
    
    context = {
    'orders':orders,
    
    }
    return render(request,'orders/orderlist.html',context)

def checkout(request):
    cart = Cart.objects.get(user = request.user,status='InProgress')
    
    cartItems = CartItems.objects.filter(cart = cart)
    
    deliveryFee = DeliveryFee.objects.last().fee
    
    discount = 0
    
    subTotal = cart.cart_total
    
    total = round(subTotal + deliveryFee,2)
    
    context = {
    'cartItems':cartItems,
    'deliveryFee':deliveryFee,
    'subTotal':subTotal,
    'discount':discount,
    'total':total,
    
    }


    return render(request,'orders/checkout.html',context)
    

def add_to_cart(request):
    product = Product.objects.get(id = request.POST['product_id'])
    quantity = int(request.POST.get('quantity',1))
    cart = Cart.objects.get(user = request.user , status = 'InProgress')
    cartItems,created = CartItems.objects.get_or_create(cart = cart, product = product)
    if not created:
        cartItems.quantity += quantity
        cartItems.save()
        return redirect(f'/products/{product.slug}')
    cartItems.quantity = quantity
    cartItems.save()
    
    
    
    
    
    return redirect(f'/products/{product.slug}')
 