# cart/context_processors.py
from .models import Cart, CartItem
from django.db.models import Sum # استيراد Sum

def cart_count(request):
    cart_items_count = 0
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        session_key = request.session.session_key
        if session_key:
            cart = Cart.objects.filter(session_key=session_key).first()
        else:
            cart = None

    if cart:
        # CHANGE START: Correctly access cart items and aggregate quantity
        cart_items_count = cart.cart_items.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
        # CHANGE END

    return {'cart_items_count': cart_items_count}