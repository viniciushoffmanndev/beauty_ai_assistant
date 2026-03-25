from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "brand",
        "price",
        "discount",
        "rating",
        "review_count",
        "is_active",
        "scraped_at",
    )
    search_fields = ("name", "description", "brand")
    list_filter = ("brand", "is_active")