from django.urls import path
from apps.products.views import search_products, whatsapp_webhook

urlpatterns = [
    path("search/", search_products, name="search_products"),
    path("whatsapp/webhook/", whatsapp_webhook, name="whatsapp_webhook"),
]