from rest_framework.decorators import api_view
from rest_framework.response import Response
from elasticsearch import Elasticsearch, ConnectionError
from elasticsearch_dsl import Search, Q
from django.db.models import Q as DjangoQ
from .models import Product
from .serializers import ProductSerializer

es = Elasticsearch("http://localhost:9200",
                   basic_auth=("elastic", "130622"))  # Ajuste as credenciais conforme necessário


# Busca completa
@api_view(['GET'])
def search_products(request):
    query = request.GET.get("q", "").lower()
    page = int(request.GET.get("page", 1))
    size = int(request.GET.get("size", 10))

    if not query:
        return Response([])

    try:
        q = Q("multi_match", query=query, fields=["name^3", "description", "brand", "flavor", "target"], fuzziness="AUTO")
        s = Search(using=es, index="products").query(q).filter("term", is_active=True)
        start = (page - 1) * size
        s = s[start:start + size]

        response = s.execute()
        results = [hit.to_dict() for hit in response]

        return Response({
            "page": page,
            "size": size,
            "total": response.hits.total.value,
            "results": results
        })

    except ConnectionError:
        # fallback ORM
        queryset = Product.objects.filter(is_active=True).filter(
            DjangoQ(name__icontains=query) |
            DjangoQ(description__icontains=query) |
            DjangoQ(brand__icontains=query)
        )
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)


# Autocomplete
@api_view(['GET'])
def autocomplete_products(request):
    query = request.GET.get("q", "").lower()

    if not query:
        return Response([])

    try:
        q = Q("multi_match", query=query, fields=["name^3", "brand", "flavor", "target"], type="phrase_prefix", fuzziness="AUTO")
        s = Search(using=es, index="products").query(q).filter("term", is_active=True)[:5]
        response = s.execute()

        suggestions = []
        for hit in response:
            suggestions.append({
                "id": hit.meta.id,
                "name": hit.name,
                "brand": hit.brand,
                "flavor": hit.flavor,
                "target": hit.target
            })

        return Response(suggestions)

    except ConnectionError:
        return Response([])