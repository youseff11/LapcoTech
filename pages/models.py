from django.db import models
from django.urls import reverse

class DailyOffer(models.Model):
    title = models.CharField(max_length=200, verbose_name="Offer Title")
    subtitle = models.CharField(max_length=255, blank=True, verbose_name="Brief Offer Description")
    image = models.ImageField(upload_to='daily_offers/%Y/%m/%d/', blank=True, verbose_name="Offer Image")
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Original Price")
    current_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Current Price")
    link_url = models.URLField(max_length=500, blank=True, verbose_name="Product/Offer Link") 
    is_active = models.BooleanField(default=True, verbose_name="Active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Daily Offer"
        verbose_name_plural = "Daily Offers"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def has_discount(self):
        return self.old_price is not None and self.old_price > self.current_price