from django.shortcuts import render,redirect
from .models import Order,Cart,CartItems
from products.models import Product


def order_list(request):
    orders = Order.objects.filter(user = request.user)
    
    context = {
    'orders':orders,
    
    }
    return render(request,'orders/orderlist.html',context)

def checkout(request):
    return render(request,'orders/checkout.html')
    

def add_to_cart(request):
    product = Product.objects.get(id = request.POST['product_id'])
    quantity = int(request.POST['quantity'])
    cart = Cart.objects.get(user = request.user , status = 'InProgress')
    cartItems,created = CartItems.objects.get_or_create(cart = cart, product = product)
    if not created:
        cartItems.quantity,cartItems.product = cartItems.quantity + quantity, product
        cartItems.save()
        return redirect(f'/products/{product.slug}')
    cartItems.quantity = quantity
    cartItems.save()
    
    
    
    
    
    return redirect(f'/products/{product.slug}')
 