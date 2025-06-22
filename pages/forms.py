from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser
from django.db import transaction
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text='Required. Enter a valid email address.',
        widget=forms.TextInput(attrs={'class': 'input_text', 'placeholder': 'Enter Email'})
    )
    phone_number = forms.CharField(
        max_length=15,
        required=False, 
        help_text='Enter your phone number (e.g., +201012345678)',
        widget=forms.TextInput(attrs={'class': 'input_text', 'placeholder': 'Enter Phone Number'})
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser 
        fields = ('username', 'email', 'phone_number',) 

        widgets = {
            'username': forms.TextInput(attrs={'class': 'input_text', 'placeholder': 'Enter Username'}),
            'password': forms.PasswordInput(attrs={'class': 'input_text', 'placeholder': 'Enter Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'input_text', 'placeholder': 'Confirm Password'}),
        }

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.phone_number = self.cleaned_data.get('phone_number')
        user.email = self.cleaned_data.get('email') 

        if commit:
            user.save()
        return user