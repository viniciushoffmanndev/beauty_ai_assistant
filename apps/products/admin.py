from django.contrib import admin
from .models import Product
from django.utils.html import format_html

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
        "image_tag",
    )
    search_fields = ("name", "description", "brand")
    list_filter = ("brand", "is_active")

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image)
        return "-"
    image_tag.short_description = "Image"
