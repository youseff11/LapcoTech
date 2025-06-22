from django.contrib import admin
from .models import Category, Brand, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

    def has_module_permission(self, request):
        return False

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

    def has_module_permission(self, request):
        return False

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'category', 'brand', 'price', 'old_price', 'is_available', 'created_at'] # <--- إضافة 'sku' هنا
    list_filter = ['is_available', 'created_at', 'category', 'brand', 'condition', 'form_factor']
    search_fields = ['name', 'description', 'cpu', 'gpu', 'ram', 'storage', 'model_name', 'sku'] # <--- إضافة 'sku' هنا
    
    fieldsets = (
        (None, {
            'fields': ('name', 'sku', 'category', 'brand', 'image', 'is_available') # <--- إضافة 'sku' هنا
        }),
        ('Pricing', {
            'fields': ('price', 'old_price')
        }),
        ('Specifications', {
            'fields': (
                'condition', 'model_name', 'cpu', 'gpu', 'ram', 'storage',
                'storage_config', 'form_factor', 'screen_size', 'refresh_rate',
                'screen_resolution', 'keyboard_language', 'warranty',
            ),
            'description': 'Enter detailed product specifications here.'
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    readonly_fields = ('created_at', 'updated_at')

    def save_model(self, request, obj, form, change):
        description_parts = []
        if obj.brand and obj.model_name:
            description_parts.append(f"{obj.brand.name} {obj.model_name}")
        elif obj.model_name:
            description_parts.append(obj.model_name)
        elif obj.name:
            description_parts.append(obj.name)

        specs_list = []
        if obj.cpu:
            specs_list.append(f"CPU: {obj.cpu}")
        if obj.gpu:
            specs_list.append(f"GPU: {obj.gpu}")
        if obj.ram:
            specs_list.append(f"RAM: {obj.ram}")
        if obj.storage:
            specs_list.append(f"Storage: {obj.storage}")
        if obj.screen_size:
            screen_info = f"{obj.screen_size}\""
            if obj.screen_resolution:
                screen_info += f" {obj.screen_resolution.replace('X', 'x')}"
            specs_list.append(screen_info)
        if obj.refresh_rate:
            specs_list.append(f"Refresh Rate: {obj.refresh_rate}")
        if obj.condition:
            specs_list.append(f"Condition: {obj.get_condition_display()}")

        if specs_list:
            description_parts.append(", ".join(specs_list))

        obj.description = ". ".join(description_parts) + "."
        super().save_model(request, obj, form, change)