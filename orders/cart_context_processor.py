from .models import Cart , CartItems

def getOrCreateCart(request):
    if request.user.is_authenticated:
        cart,created =  Cart.objects.get_or_create(user=request.user,status ='InProgress')   

        if not created:
            cart_items = CartItems.objects.filter(cart=cart)
            return {'cart_data':cart , 'cart_items':cart_items}
        return {'cart_data':cart}
    else:
        return {}