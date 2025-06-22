from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm # Make sure to import your ContactForm

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact:contact_success') # Redirect to success page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()
    return render(request, 'contact/contact.html', {'form': form})

def contact_success_view(request):
    return render(request, 'contact/contact_success.html')