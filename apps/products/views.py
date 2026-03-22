from rest_framework.decorators import api_view
from rest_framework.response import Response
from elasticsearch import ConnectionError
from elasticsearch_dsl import Search, Q
from django.db.models import Q as DjangoQ
from .models import Product
from .serializers import ProductSerializer
from .es_client import es  # cliente centralizado com basic_auth

@api_view(['GET'])
def search_products(request):
    query = request.GET.get("q", "").lower()
    page = int(request.GET.get("page", 1))
    size = int(request.GET.get("size", 10))
    mode = request.GET.get("mode", "default")  
    # mode pode ser "autocomplete" ou "default"

    if not query:
        return Response([])

    try:
        if mode == "autocomplete":
            # Autocomplete rápido com phrase_prefix
            q = Q("multi_match", query=query,
                  fields=["name^3", "brand", "flavor", "target"],
                  type="phrase_prefix")
            s = Search(using=es, index="products").query(q).filter("term", is_active=True)[:5]
            response = s.execute()

            results = [
                {
                    "id": hit.meta.id,
                    "name": hit.name,
                    "brand": hit.brand,
                    "flavor": hit.flavor,
                    "target": hit.target
                }
                for hit in response
            ]
            return Response(results)

        else:
            # Busca completa com fuzziness
            q = Q("multi_match", query=query,
                  fields=["name^3", "description", "brand", "flavor", "target"],
                  fuzziness="AUTO")
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