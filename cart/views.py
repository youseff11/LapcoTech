from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from shop.models import Product
from .models import Cart, CartItem, ShippingAddress, Order, OrderItem
from .forms import ShippingAddressForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Sum
from django.db import transaction
from django.contrib.auth import get_user_model
from django.contrib import messages

User = get_user_model()

def _get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart

@require_POST
def add_to_cart(request):
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))

        if not product_id:
            return JsonResponse({'success': False, 'message': 'Product ID is required.'}, status=400)

        product = get_object_or_404(Product, id=product_id)
        cart = _get_or_create_cart(request)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': quantity})

        if not created:
            cart_item.quantity += quantity
            cart_item.save()
            message = f"Added {quantity} more of {product.name} to your cart."
        else:
            message = f"{product.name} has been added to your cart."

        cart_items_count = cart.cart_items.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0

        return JsonResponse({'success': True, 'message': message, 'cart_items_count': cart_items_count})
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON format.'}, status=400)
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Product not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'An unexpected error occurred: {str(e)}'}, status=500)

@require_POST
def update_cart_item_quantity(request):
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        quantity_change = data.get('quantity_change')

        cart_item = get_object_or_404(CartItem, id=item_id)
        cart = _get_or_create_cart(request)

        if cart_item.cart != cart:
            return JsonResponse({'success': False, 'message': 'Unauthorized action.'}, status=403)

        new_quantity = cart_item.quantity + quantity_change

        item_removed = False
        if new_quantity <= 0:
            cart_item_id = cart_item.id
            cart_item.delete()
            message = "Item removed from cart."
            item_removed = True
        else:
            cart_item.quantity = new_quantity
            cart_item.save()
            message = "Cart item quantity updated."

        cart_items = cart.cart_items.all()
        total_cart_price = float(sum(item.total_price for item in cart_items)) if cart_items.exists() else 0.0
        cart_items_count = cart.cart_items.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0

        new_total_price_item_val = float(cart_item.total_price) if not item_removed else 0.0

        return JsonResponse({
            'success': True,
            'message': message,
            'new_quantity': cart_item.quantity if not item_removed else 0,
            'new_total_price_item': new_total_price_item_val,
            'total_cart_price': total_cart_price,
            'cart_items_count': cart_items_count,
            'item_id': item_id,
            'item_removed': item_removed
        })
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON format.'}, status=400)
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Cart item not found or already removed.'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'An unexpected error occurred: {str(e)}'}, status=500)

@require_POST
def remove_from_cart(request):
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')

        cart_item = get_object_or_404(CartItem, id=item_id)
        cart = _get_or_create_cart(request)

        if cart_item.cart != cart:
            return JsonResponse({'success': False, 'message': 'Unauthorized action.'}, status=403)

        cart_item.delete()
        message = "Item successfully removed from your cart."

        cart_items = cart.cart_items.all()
        total_cart_price = float(sum(item.total_price for item in cart_items)) if cart_items.exists() else 0.0
        cart_items_count = cart.cart_items.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0

        return JsonResponse({
            'success': True,
            'message': message,
            'total_cart_price': total_cart_price,
            'cart_items_count': cart_items_count,
            'item_id': item_id
        })
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON format.'}, status=400)
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Cart item not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'An unexpected error occurred: {str(e)}'}, status=500)

def cart_detail(request):
    try:
        cart = _get_or_create_cart(request)
        cart_items = cart.cart_items.all()

        total_cart_price = float(sum(item.total_price for item in cart_items)) if cart_items.exists() else 0.0
        cart_items_count = cart.cart_items.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0

        return render(request, 'cart/cart_detail.html', {
            'cart': cart,
            'cart_items': cart_items,
            'total_cart_price': total_cart_price,
            'cart_items_count': cart_items_count
        })
    except Exception as e:
        print(f"Error in cart_detail view: {e}")
        return render(request, 'error.html', {'error_message': 'Could not load cart details.'}, status=500)

@login_required
def checkout_page_view(request):
    cart = _get_or_create_cart(request)
    cart_items = cart.cart_items.all()
    total_cart_price = float(sum(item.total_price for item in cart_items)) if cart_items.exists() else 0.0

    initial_data = {}
    if request.user.is_authenticated:
        initial_data['first_name'] = request.user.first_name if request.user.first_name else ''
        initial_data['last_name'] = request.user.last_name if request.user.last_name else ''
        initial_data['email'] = request.user.email if request.user.email else ''
        if hasattr(request.user, 'phone_number') and request.user.phone_number:
            initial_data['phone_number'] = request.user.phone_number

    form = ShippingAddressForm(initial=initial_data)

    cart_items_data = []
    for item in cart_items:
        cart_items_data.append({
            'id': item.id,
            'product_id': item.product.id,
            'product_name': item.product.name,
            'quantity': item.quantity,
            'price': float(item.product.price),
            'total_price': float(item.total_price),
        })

    cart_data_for_json = {
        'id': cart.id,
        'total_price': total_cart_price,
        'items': cart_items_data,
        'items_count': cart.cart_items.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
    }

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_cart_price': total_cart_price,
        'cart_data_json': json.dumps(cart_data_for_json),
        'form': form,
    }
    return render(request, 'cart/checkout.html', context)

@require_POST
@login_required
def place_order(request):
    try:
        data = json.loads(request.body)
        shipping_data = data.get('shipping_info', {})

        cart = _get_or_create_cart(request)
        if not cart.cart_items.exists():
            return JsonResponse({'success': False, 'message': 'Your cart is empty. Please add items before placing an order.'}, status=400)

        with transaction.atomic():
            shipping_address_instance = None
            try:
                # Attempt to get an existing ShippingAddress linked to the current cart
                shipping_address_instance = ShippingAddress.objects.get(cart=cart)
            except ShippingAddress.DoesNotExist:
                if request.user.is_authenticated:
                    try:
                        shipping_address_instance = ShippingAddress.objects.get(user=request.user, cart__isnull=True)
                    except ShippingAddress.DoesNotExist:
                        pass
                    
            form = ShippingAddressForm(shipping_data, instance=shipping_address_instance)

            if form.is_valid():
                shipping_address = form.save(commit=False)
                if request.user.is_authenticated:
                    shipping_address.user = request.user
                    
                    # Update first_name and last_name for the logged-in user
                    user = request.user
                    user.first_name = shipping_data.get('first_name', '')
                    user.last_name = shipping_data.get('last_name', '')
                    # If you also want to update phone_number, uncomment the line below
                    # user.phone_number = shipping_data.get('phone_number', user.phone_number)
                    user.save()

                # Link the shipping address to the current cart
                shipping_address.cart = cart
                shipping_address.save()

                order = Order.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    shipping_address=shipping_address,
                    total_price=cart.total_price,
                    status='Pending'
                )

                for cart_item in cart.cart_items.all():
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        quantity=cart_item.quantity,
                        price=cart_item.product.price,
                        total_price=cart_item.total_price
                    )

                cart.cart_items.all().delete()
                
                messages.success(request, 'Your order has been placed successfully!')

                return JsonResponse({'success': True, 'message': 'Order placed successfully!', 'redirect_url': reverse('cart:order_success', args=[order.id])})

            else:
                print("Form errors:", form.errors)
                return JsonResponse({'success': False, 'message': 'Please correct the errors in your shipping information.', 'errors': form.errors}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON format.'}, status=400)
    except Exception as e:
        print(f"Error placing order: {e}")
        return JsonResponse({'success': False, 'message': f'An unexpected error occurred: {str(e)}'}, status=500)

def check_user_authentication(request):
    try:
        if request.user.is_authenticated:
            checkout_url = reverse('cart:checkout_page')
            return JsonResponse({'success': True, 'is_authenticated': True, 'redirect_url': checkout_url})
        else:
            login_url = reverse('login')
            return JsonResponse({'success': False, 'is_authenticated': False, 'message': 'You need to log in to proceed to checkout.', 'redirect_url': login_url})
    except Exception as e:
        return JsonResponse({'success': False, 'is_authenticated': False, 'message': f'Server error checking authentication: {str(e)}'}, status=500)
    
@login_required 
def order_success_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order)
    
    context = {
        'order': order,
        'order_items': order_items
    }
    return render(request, 'cart/order_success.html', context)