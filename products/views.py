from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseBadRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib import messages
from django.db import transaction
from django.views.decorators.http import require_POST

import razorpay

from .models import Product, Cart, CartItem, Order, OrderItem

# Razorpay client using keys from settings.py
client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)


def _get_cart_items_and_total(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    cart_items = list(cart.items.select_related('product'))
    total_price = sum(item.total_price() for item in cart_items)
    return cart, cart_items, total_price


def _validate_cart_stock(cart_items):
    if not cart_items:
        return "Your cart is empty."

    for item in cart_items:
        if item.quantity > item.product.stock:
            return f"Only {item.product.stock} item(s) available for {item.product.name}."

    return None


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
    if product.stock <= 0:
        messages.error(request, "This product is out of stock.")
        return redirect('product_detail', product_id=product.id)

    cart, _ = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1},
    )

    if not created:
        if cart_item.quantity >= product.stock:
            messages.error(request, "Not enough stock available.")
            return redirect('cart_view')
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
        if qty > cart_item.product.stock:
            messages.error(request, "Not enough stock available.")
            return redirect("cart_view")
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
@ensure_csrf_cookie
def checkout(request):
    """Show checkout summary. No database order is created here."""
    _, cart_items, total_price = _get_cart_items_and_total(request.user)

    if total_price == 0:
        messages.error(request, "Your cart is empty.")
        return redirect('product_list')

    stock_error = _validate_cart_stock(cart_items)
    if stock_error:
        messages.error(request, stock_error)
        return redirect('cart_view')

    context = {
        "cart_items": cart_items,
        "total_price": total_price,
        "razorpay_key_id": settings.RAZORPAY_KEY_ID,
        "user": request.user,
    }
    return render(request, 'products/checkout.html', context)


@login_required
@require_POST
def create_razorpay_order(request):
    """Create only a Razorpay order. Do not create our Order model yet."""
    _, cart_items, total_price = _get_cart_items_and_total(request.user)
    stock_error = _validate_cart_stock(cart_items)
    if stock_error:
        return JsonResponse({"error": stock_error}, status=400)

    if total_price <= 0:
        return JsonResponse({"error": "Your cart is empty."}, status=400)

    razorpay_amount = int(total_price * 100)

    try:
        razorpay_order = client.order.create({
            "amount": razorpay_amount,
            "currency": "INR",
            "payment_capture": 1,
            "notes": {"user_id": str(request.user.id)},
        })
    except razorpay.errors.BadRequestError as exc:
        return JsonResponse({"error": f"Payment setup failed: {exc}"}, status=400)
    except Exception:
        return JsonResponse(
            {"error": "Payment setup failed. Please check Razorpay keys and try again."},
            status=500,
        )

    return JsonResponse({
        "key": settings.RAZORPAY_KEY_ID,
        "amount": razorpay_amount,
        "currency": "INR",
        "order_id": razorpay_order["id"],
    })


@login_required
@require_POST
def verify_payment(request):
    """Verify Razorpay payment and create the real order after success."""
    razorpay_order_id = request.POST.get("razorpay_order_id")
    razorpay_payment_id = request.POST.get("razorpay_payment_id")
    razorpay_signature = request.POST.get("razorpay_signature")

    if not all([razorpay_order_id, razorpay_payment_id, razorpay_signature]):
        return JsonResponse({"error": "Missing Razorpay payment details."}, status=400)

    if Order.objects.filter(razorpay_payment_id=razorpay_payment_id).exists():
        return JsonResponse({"redirect_url": "/products/order-success/"})

    params_dict = {
        "razorpay_order_id": razorpay_order_id,
        "razorpay_payment_id": razorpay_payment_id,
        "razorpay_signature": razorpay_signature,
    }

    try:
        client.utility.verify_payment_signature(params_dict)
    except razorpay.errors.SignatureVerificationError:
        return JsonResponse({"error": "Payment verification failed."}, status=400)

    cart, cart_items, total_price = _get_cart_items_and_total(request.user)
    stock_error = _validate_cart_stock(cart_items)
    if stock_error:
        return JsonResponse({"error": stock_error}, status=400)

    expected_amount = int(total_price * 100)
    try:
        payment = client.payment.fetch(razorpay_payment_id)
    except Exception:
        return JsonResponse({"error": "Unable to verify payment amount."}, status=400)

    if payment.get("order_id") != razorpay_order_id:
        return JsonResponse({"error": "Payment order mismatch."}, status=400)

    if int(payment.get("amount", 0)) != expected_amount:
        return JsonResponse({"error": "Payment amount does not match cart total."}, status=400)

    if payment.get("status") != "captured":
        return JsonResponse({"error": "Payment is not successful yet."}, status=400)

    try:
        with transaction.atomic():
            if Order.objects.select_for_update().filter(razorpay_payment_id=razorpay_payment_id).exists():
                return JsonResponse({"redirect_url": "/products/order-success/"})

            product_ids = [item.product_id for item in cart_items]
            products = {
                product.id: product
                for product in Product.objects.select_for_update().filter(id__in=product_ids)
            }

            for item in cart_items:
                product = products[item.product_id]
                if item.quantity > product.stock:
                    return JsonResponse(
                        {"error": f"Insufficient stock for {item.product.name}."},
                        status=400,
                    )

            order = Order.objects.create(
                user=request.user,
                amount=total_price,
                razorpay_order_id=razorpay_order_id,
                razorpay_payment_id=razorpay_payment_id,
                razorpay_signature=razorpay_signature,
                status='paid',
                payment_status='SUCCESS',
                order_status='PLACED',
            )

            order_items = []
            for item in cart_items:
                product = products[item.product_id]
                product.stock -= item.quantity
                product.save(update_fields=['stock'])

                order_items.append(OrderItem(
                    order=order,
                    product=product,
                    product_name=product.name,
                    quantity=item.quantity,
                    price=product.price,
                ))

            OrderItem.objects.bulk_create(order_items)
            cart.items.all().delete()
    except Exception:
        return JsonResponse({"error": "Order creation failed. Please contact support."}, status=500)

    return JsonResponse({"redirect_url": "/products/order-success/"})


# -----------------------------
# Order success page
# -----------------------------
@login_required
def order_success(request):
    return render(request, 'products/order_success.html')


@login_required
def order_history(request):
    orders = (
        Order.objects.filter(user=request.user, payment_status='SUCCESS')
        .prefetch_related('items')
        .order_by('-created_at')
    )
    return render(request, 'products/order_history.html', {'orders': orders})
