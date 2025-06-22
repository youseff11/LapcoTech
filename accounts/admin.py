# project/accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from .models import CustomUser 

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'is_staff') 
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number')}), 
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_number') 

admin.site.register(CustomUser, CustomUserAdmin)