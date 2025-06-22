# myaccount/forms.py
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        # تأكد أن 'phone_number' موجود في نموذج المستخدم الخاص بك (settings.AUTH_USER_MODEL)
        # إذا لم يكن موجودًا، سيؤدي هذا إلى خطأ.
        # إذا كان في نموذج Profile منفصل، فستحتاج لتعديل هذا الفورم.
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number'] # أضفت first_name, last_name للاكتمال

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'readonly': 'readonly'}), 
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number (e.g., +2010...)', 'pattern': r'^\+?[0-9]{10,15}$', 'title': 'Enter a valid phone number (e.g., +2010...)'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # يمكنك إضافة خصائص إضافية للحقول هنا، مثل جعل بعضها مطلوبًا
        # self.fields['first_name'].required = True 
        # self.fields['last_name'].required = True