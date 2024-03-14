from django.shortcuts import render,redirect , get_object_or_404
from .models import Order,Cart,CartItems,Coupon ,OrderItems
import datetime
from django.http import JsonResponse
from django.template.loader import render_to_string

from django.conf import settings
import stripe

from products.models import Product
from settings.models import DeliveryFee
from accounts.models import Adress
from utils.generate_code import generate_code
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
    pub_key = settings.STRIPE_API_KEY_PUBLISHABLE

    if request.method == 'POST':
        code = request.POST['coupon_code']
        coupon = get_object_or_404(Coupon,code = code)
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
                context = {
                 'cartItems':cartItems,
                 'deliveryFee':deliveryFee,
                 'subTotal':subTotal,
                 'discount':coupon_value,
                 'total':total,
                 'pub_key':pub_key
                }
                return render(request,'orders/checkout.html',context)
    
    
    discount = 0
    
    subTotal = cart.cart_total
    
    total = round(subTotal + deliveryFee,2)
    
    context = {
    'cartItems':cartItems,
    'deliveryFee':deliveryFee,
    'subTotal':subTotal,
    'discount':discount,
    'total':total,
    'pub_key':pub_key
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
    #ajax
    cart = Cart.objects.get(user = request.user , status = 'InProgress')
    cartItems = CartItems.objects.filter(cart = cart)
    total = cart.cart_total
    cartCount  = len(cartItems)
    cartItems = render_to_string('includes/cart.html',{'cart_items':cartItems , 'cartdata':cart})
   
    return JsonResponse({'result':cartItems , 'total':total,'cart_count':cartCount})


def payment_process(request):
    cart = Cart.objects.get(user = request.user,status = 'InProgress')
    delivery_fee = DeliveryFee.objects.last().fee
    if cart.total_after_coupon:
        total = cart.total_after_coupon + delivery_fee
    else:
        total = cart.cart_total + delivery_fee
        
    #generate code to a new order
    code = generate_code()
    #using djagno sessions
    request.session['order_code'] = code 
    request.session.save()
    #create invoice in strip
    
    stripe.api_key = settings.STRIPE_API_KEY_SECRET
    DOMAIN = 'http://127.0.0.1:8000/'
    checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price_data':{
                        'currency':'usd',
                        'product_data':{'name':code},
                        'unit_amount': int(total*100)
                    },
                     'quantity': 1
                },
            ],
            mode='payment',
            success_url=DOMAIN +'orders/checkout/payment/success',
            cancel_url=DOMAIN +'orders/checkout/payment/failed'
        )
    # print(checkout_session.session.id)
    return JsonResponse({'payment_session':checkout_session})

def payment_success(request):
    cart = Cart.objects.get(user = request.user,status = 'InProgress')
    cartItems = CartItems.objects.filter(cart =cart)
    user_address = Adress.objects.get(user = request.user)
    code =request.session.get('order_code')
        
     #cart ---> order  , cartItems --->  orderItems
    new_order = Order.objects.create(
            user = request.user,
            status = 'Recieved',
            code =code  , 
            delivery_location = user_address,
            coupon = cart.coupon,
            total_after_coupon=cart.total_after_coupon,
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
    return render(request,'orders/success.html',{'code':code})
def payment_failed(request):

    return render(request,'orders/failed.html',{})

    
