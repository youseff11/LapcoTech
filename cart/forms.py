# cart/forms.py
from django import forms
from .models import ShippingAddress

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'city', 'address', 'faculty', 'year']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Address'}),
            'faculty': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Faculty (Optional)'}),
            'year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Academic Year (Optional)'}),
        }