from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'subject', 'submitted_at') # Add phone_number to list_display
    list_filter = ('submitted_at',)
    search_fields = ('name', 'email', 'phone_number', 'subject', 'message') # Add phone_number to search_fields
    readonly_fields = ('submitted_at',)