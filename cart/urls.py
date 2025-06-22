# cart/urls.py
from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/', views.add_to_cart, name='add_to_cart'),
    path('update_quantity/', views.update_cart_item_quantity, name='update_quantity'), 
    path('remove/', views.remove_from_cart, name='remove_from_cart'), 
    path('check_auth/', views.check_user_authentication, name='check_auth'),
    path('checkout/', views.checkout_page_view, name='checkout_page'),
    path('place_order/', views.place_order, name='place_order'), 
    # **السطر الوحيد الذي يجب أن يكون لـ order_success_view**
    path('order-success/<int:order_id>/', views.order_success_view, name='order_success'), 
]