# pages/admin.py

from django.contrib import admin
from .models import DailyOffer

@admin.register(DailyOffer)
class DailyOfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'current_price', 'old_price', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'subtitle')
    date_hierarchy = 'created_at'