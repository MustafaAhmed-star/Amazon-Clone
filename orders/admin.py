from django.contrib import admin
from .models import Order, OrderItems,Coupon ,Cart,CartItems
# Register your models here.
from products.models import Product
class OrderItemInline(admin.TabularInline):
    model = OrderItems


class CartAdmin(admin.ModelAdmin):
    list_display = ['user','status']
    list_filter = ['status']
    search_fields  = ['status']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    # ... other admin configuration for Order

admin.site.register(Coupon)
admin.site.register(Cart,CartAdmin)
admin.site.register(CartItems)