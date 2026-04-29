from django.contrib import admin
from .models import Product, Cart, CartItem
from .models import Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'image')
    search_fields = ('name', 'description')


admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
