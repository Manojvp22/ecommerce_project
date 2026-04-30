from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/create-razorpay-order/', views.create_razorpay_order, name='create_razorpay_order'),
    path('checkout/verify-payment/', views.verify_payment, name='verify_payment'),
    path('orders/', views.order_history, name='order_history'),
    path('order-success/', views.order_success, name='order_success'),
    
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),

    path('payment/callback/', views.verify_payment, name='payment_callback'),
]
