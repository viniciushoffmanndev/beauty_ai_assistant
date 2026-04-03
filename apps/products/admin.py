from django.contrib import admin
from django.utils.html import format_html

from .models import Product, UserSelection


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "brand",
        "category",
        "target",
        "flavor",
        "price",
        "discount",
        "rating",
        "review_count",
        "is_active",
        "scraped_at",
        "image_tag",
    )
    search_fields = ("name", "description", "brand", "external_id")
    list_filter = ("brand", "category", "target", "flavor", "is_active", "source")
    readonly_fields = ("image_preview", "scraped_at", "created_at")
    ordering = ("-scraped_at",)

    fieldsets = (
        ("Identificação", {
            "fields": ("external_id", "source")
        }),
        ("Informações básicas", {
            "fields": ("name", "brand", "description")
        }),
        ("Classificação", {
            "fields": ("target", "category", "flavor")
        }),
        ("Preço e avaliação", {
            "fields": ("price", "old_price", "discount", "rating", "review_count")
        }),
        ("Links e mídia", {
            "fields": ("url", "image", "image_preview")
        }),
        ("Controle", {
            "fields": ("is_active", "scraped_at", "created_at")
        }),
    )

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image)
        return "-"
    image_tag.short_description = "Imagem"

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 300px;" />', obj.image)
        return "No image available"
    image_preview.short_description = "Preview"


@admin.register(UserSelection)
class UserSelectionAdmin(admin.ModelAdmin):
    list_display = (
        "whatsapp_user_id",
        "product_reference_id",
        "created_at",
    )
    search_fields = ("whatsapp_user_id", "product_reference_id")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
