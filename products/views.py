from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

import razorpay

from .models import Product, Cart, CartItem, Order

# Razorpay client using keys from settings.py
client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)


# -----------------------------
# Product listing & detail
# -----------------------------
def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/product_detail.html', {'product': product})


# -----------------------------
# Cart operations
# -----------------------------
@login_required
def add_to_cart(request, product_id):
    """Add a product to the user's cart (or increase quantity)."""
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1},
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_view')


@login_required
def cart_view(request):
    """Display current user's cart; create it if missing."""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    total = sum(item.total_price() for item in items)

    context = {
        'cart': cart,
        'items': items,
        'total': total,
    }
    return render(request, 'products/cart_view.html', context)


@login_required
def update_cart_item(request, item_id):
    """Update quantity of a single CartItem."""
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request")

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user,
    )

    try:
        qty = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        qty = 1

    if qty <= 0:
        # qty 0 or negative → remove item
        cart_item.delete()
    else:
        cart_item.quantity = qty
        cart_item.save()

    return redirect("cart_view")


@login_required
def remove_cart_item(request, item_id):
    """Remove an item from the cart."""
    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user,
    )
    cart_item.delete()
    return redirect("cart_view")


# -----------------------------
# Checkout + Razorpay payment
# -----------------------------
@login_required
def checkout(request):
    """Create Razorpay order and show checkout page."""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    total_price = sum(item.total_price() for item in cart_items)

    if total_price == 0:
        messages.error(request, "Your cart is empty.")
        return redirect('product_list')

    # 1) Create our own Order record
    order = Order.objects.create(
        user=request.user,
        amount=total_price,
        status='created',
    )

    # 2) Razorpay expects amount in paise (integer)
    razorpay_amount = int(total_price * 100)

    # 3) API call to Razorpay to create an order
    razorpay_order = client.order.create({
        "amount": razorpay_amount,
        "currency": "INR",
        "payment_capture": 1,
        "notes": {"internal_order_id": str(order.id)},
    })

    # 4) Store Razorpay order id in our DB
    order.razorpay_order_id = razorpay_order["id"]
    order.save()

    context = {
        "cart_items": cart_items,
        "total_price": total_price,
        "razorpay_order_id": razorpay_order["id"],
        "razorpay_key_id": settings.RAZORPAY_KEY_ID,
        "razorpay_amount": razorpay_amount,
        "user": request.user,
    }
    return render(request, 'products/checkout.html', context)


@csrf_exempt
def payment_callback(request):
    """
    Razorpay posts here after payment.
    We verify the signature and update the Order status.
    """
    if request.method == "POST":
        data = request.POST

        razorpay_order_id = data.get("razorpay_order_id")
        razorpay_payment_id = data.get("razorpay_payment_id")
        razorpay_signature = data.get("razorpay_signature")

        if not razorpay_order_id:
            return redirect('product_list')

        try:
            order = Order.objects.get(razorpay_order_id=razorpay_order_id)
        except Order.DoesNotExist:
            return redirect('product_list')

        params_dict = {
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature,
        }

        try:
            # Verify the signature from Razorpay
            client.utility.verify_payment_signature(params_dict)
        except razorpay.errors.SignatureVerificationError:
            order.status = 'failed'
            order.save()
            # optional message if user is still logged in
            messages.error(request, "Payment verification failed.")
            return redirect('checkout')
        else:
            order.status = 'paid'
            order.razorpay_payment_id = razorpay_payment_id
            order.razorpay_signature = razorpay_signature
            order.save()

            # Clear the cart after successful payment
            cart, _ = Cart.objects.get_or_create(user=order.user)
            cart.items.all().delete()

            return redirect('order_success')

    return redirect('product_list')


# -----------------------------
# Order success page
# -----------------------------
@login_required
def order_success(request):
    return render(request, 'products/order_success.html')
