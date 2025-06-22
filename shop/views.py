from django.shortcuts import render, get_object_or_404
from django.db.models import Q 
from .models import Product, Category, Brand

def product_list(request, category_slug=None, brand_slug=None):
    category = None
    brand = None
    products = Product.objects.filter(is_available=True)
    page_title = "All Laptops" 

    # 1. Handle filtering by Category from URL slug
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        page_title = category.name 

    # 2. Handle filtering by Brand from URL slug
    if brand_slug:
        brand = get_object_or_404(Brand, slug=brand_slug)
        products = products.filter(brand=brand)

        if category_slug: 
            page_title = f"{category.name} ({brand.name})"
        else: 
            page_title = f"{brand.name} Laptops"

    # 3. Handle search query from GET request
    query = request.GET.get('q') 
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) | 
            Q(brand__name__icontains=query) |
            Q(cpu__icontains=query) | 
            Q(gpu__icontains=query) |
            Q(ram__icontains=query) |
            Q(storage__icontains=query) |
            Q(model_name__icontains=query) |
            Q(sku__icontains=query)  # <--- إضافة البحث بـ SKU
        ).distinct() 
        if page_title == "All Laptops": 
            page_title = f"Search results for '{query}'"
        else:
            page_title = f"{page_title} - Search for '{query}'"


    context = {
        'category': category,
        'brand': brand,
        'products': products,
        'page_title': page_title,
        'categories': Category.objects.all(),
        'brands': Brand.objects.all(),
        'selected_category': category,
        'selected_brand': brand,
        'query': query,
    }
    return render(request, 'shop/product_list.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_available=True)
    context = {
        'product': product,
    }
    return render(request, 'shop/product_detail.html', context)