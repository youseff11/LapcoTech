# C:\Users\magdy\OneDrive\Desktop\lapco\lapco-tech\project\cart\admin.py
from django.contrib import admin
from django.utils.html import format_html # **تأكد من استيرادها هنا**

from .models import Cart, CartItem, ShippingAddress, Order, OrderItem # استيراد النماذج من models.py

@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name', 'email', 'phone_number', 'city', 'address', 'created_at')
    list_filter = ('created_at', 'city', 'user')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number', 'address', 'city')
    readonly_fields = ('created_at', 'updated_at',)

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.user:
            return self.readonly_fields + ('first_name', 'last_name', 'email', 'phone_number')
        return self.readonly_fields


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('price', 'total_price') # ستتم مراجعة هذه الحقول في models.py


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # **تأكد أن 'colored_status' موجودة هنا**
    list_display = ('id', 'user', 'shipping_address', 'total_price', 'status', 'colored_status', 'created_at')
    list_filter = ('status', 'created_at', 'user', 'shipping_address__city')
    search_fields = ('user__username', 'shipping_address__first_name', 'shipping_address__last_name', 'id')
    readonly_fields = ('created_at', 'updated_at', 'total_price')
    raw_id_fields = ('user', 'shipping_address')
    inlines = [OrderItemInline]

    list_editable = ['status'] # هذا السطر صحيح

    # **هام جداً: تأكد أن الدالة colored_status معرفة داخل OrderAdmin**
    # **وأن مسافاتها البادئة صحيحة لتكون جزءاً من الفئة.**
    def colored_status(self, obj):
        color_map = {
            'Pending': '#facc15',
            'Processing': '#38bdf8',
            'Shipped': '#34d399',
            'Delivered': '#10b981',
            'Cancelled': '#f87171',
        }
        # تأكد من أن مفاتيح color_map تتطابق تمامًا مع قيم الخيارات في نموذجك (status_value)
        # إذا كانت قيم النموذج هي 'Pending', 'Processing', 'Shipped', الخ، فتأكد من استخدام نفس الأحرف الكبيرة/الصغيرة.
        color = color_map.get(obj.status, '#d1d5db')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 8px; border-radius: 6px;">{}</span>',
            color,
            obj.get_status_display()
        )
    colored_status.short_description = 'Status (Colored)' # الاسم الذي سيظهر للعمود
    colored_status.admin_order_field = 'status' # يسمح بالترتيب بناءً على حقل status الفعلي


    actions = ['mark_pending', 'mark_processing', 'mark_shipped', 'mark_delivered', 'mark_cancelled']

    @admin.action(description="Mark selected orders as Pending")
    def mark_pending(self, request, queryset):
        updated_count = queryset.update(status='Pending')
        self.message_user(request, f"{updated_count} order(s) marked as Pending.")

    @admin.action(description="Mark selected orders as Processing")
    def mark_processing(self, request, queryset):
        updated_count = queryset.update(status='Processing')
        self.message_user(request, f"{updated_count} order(s) marked as Processing.")

    @admin.action(description="Mark selected orders as Shipped")
    def mark_shipped(self, request, queryset):
        updated_count = queryset.update(status='Shipped')
        self.message_user(request, f"{updated_count} order(s) marked as Shipped.")

    @admin.action(description="Mark selected orders as Delivered")
    def mark_delivered(self, request, queryset):
        updated_count = queryset.update(status='Delivered')
        self.message_user(request, f"{updated_count} order(s) marked as Delivered.")

    @admin.action(description="Mark selected orders as Cancelled")
    def mark_cancelled(self, request, queryset):
        updated_count = queryset.update(status='Cancelled')
        self.message_user(request, f"{updated_count} order(s) marked as Cancelled.", level='WARNING')