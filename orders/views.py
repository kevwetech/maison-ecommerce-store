from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from .cart import Cart
from django.http import JsonResponse
from .models import Order, OrderItem, DeliveryOption
import requests
from django.conf import settings
from django.core.mail import send_mail
import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.


def cart_add(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = Cart(request)
    cart.add(product)
    
    # If AJAX request return JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': sum(item['quantity'] for item in cart.cart.values())
        })
    
    return redirect(request.META.get('HTTP_REFERER', 'products_page'))

@login_required
def cart_remove(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = Cart(request)
    cart.remove(product)
    return redirect('cart_page')

@login_required
def cart_decrease(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = Cart(request)
    cart.decrease(product)
    return redirect('cart_page')


@login_required
def cart_page(request):
    cart = Cart(request)
    product_ids = [int(pid) for pid in cart.cart.keys()]
    products = Product.objects.filter(id__in=product_ids)

    cart_items = []
    for product in products:
        item = cart.cart[str(product.id)]
        cart_items.append({
            'product': product,
            'quantity': item['quantity'],
            'price': float(item['price']),
            'subtotal': float(item['price']) * item['quantity'],
        })

    subtotal = cart.total_price()
    tax = round(subtotal * 0.08, 2)
    grand_total = round(subtotal + tax, 2)

    return render(request, 'orders/cart.html', {
        'cart_items': cart_items,
        'total': subtotal,
        'tax': tax,
        'grand_total': grand_total,
    })


@login_required
def checkout(request):
    cart = Cart(request)
    product_ids = [int(pid) for pid in cart.cart.keys()]
    products = Product.objects.filter(id__in=product_ids)
    delivery_options = DeliveryOption.objects.filter(is_active=True)

    cart_items = []
    for product in products:
        item = cart.cart[str(product.id)]
        cart_items.append({
            'product': product,
            'quantity': item['quantity'],
            'price': float(item['price']),
            'subtotal': float(item['price']) * item['quantity'],
        })

    subtotal = cart.total_price()
    tax = round(subtotal * 0.08, 2)

    if request.method == "POST":
        if not cart.cart:
            messages.error(request, "Your cart is empty.")
            return redirect('cart_page')

        # Get delivery option
        delivery_id = request.POST.get('delivery_option')
        delivery_option = get_object_or_404(DeliveryOption, pk=delivery_id)

        # Check if free shipping applies
        delivery_price = 0
        if delivery_option.free_above and subtotal >= float(delivery_option.free_above):
            delivery_price = 0
        else:
            delivery_price = float(delivery_option.price)

        grand_total = round(subtotal + tax + delivery_price, 2)

        order = Order.objects.create(
            user=request.user,
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            country=request.POST.get('country'),
            delivery_option=delivery_option,
            delivery_price=delivery_price,
        )

        for product_id, item in cart.cart.items():
            product = get_object_or_404(Product, pk=product_id)
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item['quantity'],
                price=item['price'],
            )

        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json',
        }
        data = {
            'email': order.email,
            'amount': int(grand_total * 100),
            'reference': f'order_{order.id}',
            'callback_url': request.build_absolute_uri(f'/orders/payment/verify/{order.id}/'),
            'metadata': {
                'order_id': order.id,
                'full_name': order.full_name,
            }
        }
        response = requests.post(
            'https://api.paystack.co/transaction/initialize',
            json=data,
            headers=headers
        )
        result = response.json()

        if result['status']:
            cart.clear()
            return redirect(result['data']['authorization_url'])
        else:
            order.delete()
            messages.error(request, 'Payment initialization failed. Try again.')
            return redirect('checkout')

    else:
        grand_total = round(subtotal + tax, 2)

    return render(request, 'orders/checkout.html', {
        'cart_items': cart_items,
        'total': subtotal,
        'tax': tax,
        'grand_total': grand_total,
        'delivery_options': delivery_options,
        'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY,
    })


@login_required
def payment_verify(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    reference = request.GET.get('reference')

    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
    }
    response = requests.get(
        f'https://api.paystack.co/transaction/verify/{reference}',
        headers=headers
    )
    result = response.json()

    if result['status'] and result['data']['status'] == 'success':
        order.completed = True
        order.save()
        messages.success(request, 'Payment successful! Your order has been placed.')
        return redirect('order_detail', order_id=order.id)
    else:
        messages.error(request, 'Payment failed. Please try again.')
        return redirect('checkout')





@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})


def track_order(request):
    order = None
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        email = request.POST.get('email')
        try:
            order = Order.objects.get(id=order_id, email=email)
        except Order.DoesNotExist:
            messages.error(request, 'No order found with that ID and email.')
    return render(request, 'orders/track_order.html', {'order': order})