from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # المسار العام لقائمة المنتجات (يعرض كل المنتجات)
    # هذا المسار سيستخدم الدالة الموحدة 'product_list'
    path('', views.product_list, name='product_list'),

    # المسار للفلترة حسب الفئة
    # هذا المسار سيستخدم الدالة الموحدة 'product_list' أيضًا، مع تمرير slug للفئة
    path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),

    # المسار الجديد للفلترة حسب الماركة (إذا كنت تريد إضافته)
    path('brand/<slug:brand_slug>/', views.product_list, name='product_list_by_brand'),

    # المسار الجديد للفلترة حسب الفئة والماركة (إذا كنت تريد إضافته)
    path('category/<slug:category_slug>/brand/<slug:brand_slug>/', views.product_list, name='product_list_by_category_and_brand'),

    # تفاصيل المنتج
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
]