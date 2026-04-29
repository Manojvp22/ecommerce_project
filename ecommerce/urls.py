from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
