from django.contrib import admin
from .models import Order, OrderItems , Coupon
# Register your models here.
admin.site.register(Order)
admin.site.register(OrderItems)
admin.site.register(Coupon)