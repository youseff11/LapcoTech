# myaccount/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model

from .forms import UserProfileForm 
from cart.models import Order # تحتاج لاستيراد Order من تطبيق cart

User = get_user_model()

@login_required
def myaccount(request):
    user = request.user
    # جلب الطلبات الخاصة بالمستخدم الحالي وترتيبها من الأحدث للأقدم
    orders = Order.objects.filter(user=user).order_by('-created_at') 

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user) 
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('myaccount:account') # إعادة توجيه لتجنب إعادة إرسال الفورم عند التحديث
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserProfileForm(instance=user) # تمرير كائن المستخدم للفورم لملء البيانات الحالية

    context = {
        'form': form,
        'orders': orders,
    }
    return render(request, 'myaccount/myaccount.html', context)

# إذا كنت تريد صفحة تفاصيل طلب منفصلة في myaccount بدلاً من استخدام cart:order_success
# @login_required
# def order_details(request, order_id):
#     order = get_object_or_404(Order, id=order_id, user=request.user)
#     order_items = OrderItem.objects.filter(order=order)
#     context = {
#         'order': order,
#         'order_items': order_items
#     }
#     return render(request, 'myaccount/order_details.html', context) # تحتاج لإنشاء قالب order_details.html