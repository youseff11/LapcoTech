# pages/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm

# استورد موديل DailyOffer الجديد
from .models import DailyOffer 

# --- 1. User Authentication & Authorization Views ---

# ... (كود الـ login, signup, logout زي ما هو) ...

def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}! You are logged in.')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = AuthenticationForm()
    return render(request, 'pages/login.html', {'form': form})

def user_signup(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account for {user.username} created successfully! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')

    else: 
        form = CustomUserCreationForm()
    return render(request, 'pages/signup.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')

# --- 2. General Page Views ---

def home(request):
    # جلب العروض اليومية النشطة
    daily_offers = DailyOffer.objects.filter(is_active=True)
    
    context = {
        'daily_offers': daily_offers,
    }
    return render(request, 'pages/home.html', context)

def policies(request):
    return render(request, 'pages/policies.html')