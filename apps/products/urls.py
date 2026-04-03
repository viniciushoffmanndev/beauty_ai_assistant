from django.urls import path

from apps.products.api_views import search_products
from apps.products.webhook.views import whatsapp_webhook

urlpatterns = [
    path("search/", search_products, name="search_products"),
    path("whatsapp/webhook/", whatsapp_webhook, name="whatsapp_webhook"),
]
