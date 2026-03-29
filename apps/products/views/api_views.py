from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.products.services import search_products_in_es


@api_view(["GET"])
def search_products(request):
    query = request.GET.get("q", "").strip()

    if not query:
        return Response([])

    products = search_products_in_es(query=query, size=20)
    return Response(products)   