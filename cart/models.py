# C:\Users\magdy\OneDrive\Desktop\lapco\lapco-tech\project\cart\models.py
from django.db import models
from django.conf import settings
from shop.models import Product # تأكد أن هذا المسار صحيح لنموذج المنتج الخاص بك
from django.utils import timezone
from decimal import Decimal # *** مهم جداً: استورد Decimal هنا ***

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user:
            return f"Cart for {self.user.username}"
        return f"Cart {self.id} (Guest - {self.session_key[:5] if self.session_key else 'No Session'})"

    @property
    def total_price(self):
        # الآن 'total_price' هو حقل فعلي في CartItem، فـ Sum عليه هيشتغل
        # استخدم Decimal('0.00') كقيمة افتراضية عشان تتجنب مشاكل التوافق مع DecimalField
        return self.cart_items.aggregate(total_sum=models.Sum('total_price'))['total_sum'] or Decimal('0.00')


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    # **السطر ده هو الحل الرئيسي لمشكلتك الحالية: total_price أصبح حقل دائم**
    total_price = models.DecimalField(max_digits=10, decimal_places=0, default=0) # بما أنك تريدها قيمة صحيحة

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Cart {self.cart.id}"

    # **أضف دالة save دي عشان تحسب قيمة total_price وتخزنها قبل الحفظ**
    def save(self, *args, **kwargs):
        # تأكد من أن product.price هو DecimalField أو قم بتحويله
        # لو product.price هو float أو int، يجب تحويله لـ Decimal أولاً
        if self.product and self.product.price is not None:
            # هنا بنضمن أن الناتج هو Decimal و بدون كسور عشرية (مثل ما تريد)
            self.total_price = Decimal(str(self.quantity * self.product.price)).quantize(Decimal('1'))
        else:
            self.total_price = Decimal('0')
        super().save(*args, **kwargs)


class ShippingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    # **تأكد أن هذا السطر موجود كما ناقشنا سابقاً**
    cart = models.OneToOneField(Cart, on_delete=models.SET_NULL, null=True, blank=True, related_name='shipping_address')

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.address}, {self.city}"

    class Meta:
        verbose_name_plural = "Shipping addresses"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    # بما أنك تريدها قيمة صحيحة
    total_price = models.DecimalField(max_digits=10, decimal_places=0, default=0)

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username if self.user else 'Guest'}"

    @property
    def get_order_total(self):
        # هذا property سيعمل بشكل صحيح طالما price و quantity في OrderItem هما DecimalField
        return sum(item.get_total for item in self.order_items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    # بما أنك تريدها قيمة صحيحة
    price = models.DecimalField(max_digits=10, decimal_places=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=0)

    def __str__(self):
        return f"{self.quantity} x {self.product.name if self.product else 'Deleted Product'}"

    @property
    def get_total(self):
        return self.price * self.quantity # هتكون Decimal * int/Decimal, والناتج هيكون Decimal