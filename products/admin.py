from django.contrib import admin
from .models import Product, Cart, CartItem
from .models import Order

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)