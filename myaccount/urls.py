# myaccount/urls.py
from django.urls import path
from . import views

app_name = 'myaccount' 

urlpatterns = [
    path('', views.myaccount, name='account'),
    # قد تحتاج مسارًا لتفاصيل الطلب إذا لم تستخدم order_success من تطبيق cart
    # path('orders/<int:order_id>/', views.order_details, name='order_details'), 
]