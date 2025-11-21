from django.contrib import admin
from django.urls import path, include
from products import views as product_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home page → product list
    path('', product_views.product_list, name='product_list'),

    # Products app URLs
    path('products/', include('products.urls')),

    # Accounts (auth) URLs
    path('accounts/', include('accounts.urls')),
]
