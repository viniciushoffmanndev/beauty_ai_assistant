from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from apps.products.services.product_search_service import ProductSearchService


search_service = ProductSearchService()


@api_view(["GET"])
def search_products(request):
    query = request.GET.get("q", "").strip()
    size = request.GET.get("size", 20)

    try:
        size = int(size)
    except (TypeError, ValueError):
        size = 20

    size = max(1, min(size, 50))

    if not query:
        return Response([], status=status.HTTP_200_OK)

    products = search_service.search(query=query, size=size)
    return Response(products, status=status.HTTP_200_OK)
