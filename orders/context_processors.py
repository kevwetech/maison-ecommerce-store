from .cart import Cart



def cart_count(request):
    try:
        if request.user.is_authenticated:
            cart = Cart(request)
            count = sum(item['quantity'] for item in cart.cart.values())
            return {'cart_count': count}
        return {'cart_count': 0}
    except Exception:
        return {'cart_count': 0}