from django.urls import path
from .views import search_products, whatsapp_webhook

urlpatterns = [
    path('search/', search_products, name="search_products"),
    path("search_products/", search_products, name="search_products"),
    path("whatsapp_webhook/", whatsapp_webhook, name="whatsapp_webhook")
]