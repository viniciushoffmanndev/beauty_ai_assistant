from django.urls import path
from .views import search_products, autocomplete_products

urlpatterns = [
    path('search/', search_products, name="search_products"),
    path('autocomplete/', autocomplete_products, name="autocomplete_products"),
]