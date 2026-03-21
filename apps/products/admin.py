from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "brand", "category", "price", "is_active")
    search_fields = ("name", "description", "brand")
    list_filter = ("category", "brand", "is_active")