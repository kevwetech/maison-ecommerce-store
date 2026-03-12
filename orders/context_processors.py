from .cart import Cart

def cart_count(request):
    if request.user.is_authenticated:
        cart = Cart(request)
        count = sum(item['quantity'] for item in cart.cart.values())
        return {'cart_count': count}
    return {'cart_count': 0}