from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, help_text="A URL-friendly short label for the category.")

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, help_text="A URL-friendly short label for the brand.")
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Brands"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list')


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, help_text="The category this product belongs to.")
    brand = models.ForeignKey(Brand, related_name='products', on_delete=models.SET_NULL, null=True, blank=True, help_text="The brand of this product.")
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True) 
    price = models.DecimalField(max_digits=10, decimal_places=0)
    old_price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, help_text="Original price before discount (optional).")

    # --- التعديل هنا: إضافة حقل SKU ---
    sku = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True,
        help_text="Stock Keeping Unit (Unique Identifier for the product)"
    )
    # ----------------------------------

    CONDITION_CHOICES = [
        ('NEW', 'New'),
        ('USED', 'Used'),
        ('REFURBISHED', 'Refurbished'),
        ('OPEN_BOX', 'Open Box'),
        ('ESTERAD', 'استيراد'), # <--- تم إضافة "ESTERAD" هنا
    ]
    condition = models.CharField(
        max_length=50,
        choices=CONDITION_CHOICES,
        blank=True,
        null=True,
        help_text="e.g., New, Used: Grade A, Refurbished"
    )

    model_name = models.CharField(max_length=100, blank=True, null=True, help_text="Specific model name (e.g., Inspiron 3501)")
    cpu = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., Intel Core i3-1005G1")
    gpu = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., Intel Iris Plus G1, NVIDIA GeForce RTX 3050")
    ram = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., 8GB, 16GB DDR4")
    storage = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., 128GB, 512GB SSD, 1TB HDD")
    storage_config = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., 128GB SSD, 512GB NVMe SSD")
    form_factor = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., Business, Gaming, 2-in-1")
    screen_size = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., 15.6 inch, 13.3 inch")
    refresh_rate = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., 60Hz, 120Hz")
    screen_resolution = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., 1920x1080, 1366x768")
    keyboard_language = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., EN, AR")
    warranty = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., 3 Months, 1 Year")

    image = models.ImageField(upload_to='products/', blank=True, null=True, help_text="Upload an image for the product.")
    is_available = models.BooleanField(default=True, help_text="Is this product currently available for purchase?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name'] 
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['brand']),
            models.Index(fields=['category', 'brand']),
            models.Index(fields=['sku']), # <--- إضافة فهرس لـ SKU لتحسين البحث
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[str(self.id)])

    @property
    def get_product_specs_description(self):
        """
        Generates a formatted description string using specific product specifications:
        Model Name, Form Factor, Screen Size, CPU, GPU, RAM.
        """
        specs = []

        if self.brand and self.model_name:
            specs.append(f"{self.brand.name} {self.model_name}")
        elif self.model_name:
            specs.append(self.model_name)
        
        if self.form_factor:
            specs.append(self.form_factor)
            
        if self.screen_size:
            screen_info = f"{self.screen_size}\""
            if self.screen_resolution:
                screen_info += f" {self.screen_resolution.replace('X', 'x')}"
            specs.append(screen_info)
            
        if self.cpu:
            if "Intel Core" not in self.cpu and "AMD Ryzen" not in self.cpu:
                specs.append(f"CPU: {self.cpu}")
            else:
                specs.append(f"CPU: {self.cpu}")
        
        if self.gpu:
            if "Intel" not in self.gpu and "NVIDIA" not in self.gpu and "AMD" not in self.gpu:
                specs.append(f"GPU: {self.gpu}")
            else:
                specs.append(f"GPU: {self.gpu}")
        
        if self.ram:
            specs.append(f"{self.ram} RAM")
        
        if self.storage:
            specs.append(f"{self.storage} Storage")

        if self.keyboard_language:
            specs.append(f"Keyboard: {self.keyboard_language}")

        return ", ".join(specs)