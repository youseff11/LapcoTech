from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone_number', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Your Phone Number '}), 
            'subject': forms.TextInput(attrs={'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'placeholder': 'Your Message', 'rows': 5}),
        }
        labels = {
            'name': 'Your Name',
            'email': 'Your Email',
            'phone_number': 'Your phone_number',
            'subject': 'Subject',
            'message': 'Your Message',
        }