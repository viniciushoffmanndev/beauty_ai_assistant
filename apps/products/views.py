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
    target = request.GET.get("target", None)

    if not query:
        return Response([])

    try:
        # tokens da query
        tokens = query.split()

        if mode == "autocomplete":
            q = Q("multi_match", query=query,
                  fields=["name^3", "brand", "flavor", "target"],
                  type="phrase_prefix")
            s = Search(using=es, index="products").query(q).filter("term", is_active=True)

            # aplica filtros automáticos
            if "feminino" in tokens:
                s = s.filter("term", target="feminino")
            elif "masculino" in tokens:
                s = s.filter("term", target="masculino")

            if "cítrico" in tokens:
                s = s.filter("term", flavor="cítrico")
            elif "amadeirado" in tokens:
                s = s.filter("term", flavor="amadeirado")

            s = s[:5]
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
            q = Q("multi_match", query=query,
                  fields=["name^3", "description", "brand", "flavor", "target"],
                  fuzziness="AUTO")
            s = Search(using=es, index="products").query(q).filter("term", is_active=True)

            # aplica filtros automáticos
            if "feminino" in tokens:
                s = s.filter("term", target="feminino")
            elif "masculino" in tokens:
                s = s.filter("term", target="masculino")

            if "cítrico" in tokens:
                s = s.filter("term", flavor="cítrico")
            elif "amadeirado" in tokens:
                s = s.filter("term", flavor="amadeirado")

            if target:
                s = s.filter("term", target=target)

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
        queryset = Product.objects.filter(is_active=True).filter(
            DjangoQ(name__icontains=query) |
            DjangoQ(description__icontains=query) |
            DjangoQ(brand__icontains=query)
        )

        # aplica filtros automáticos também no fallback ORM
        if "feminino" in query:
            queryset = queryset.filter(target="feminino")
        elif "masculino" in query:
            queryset = queryset.filter(target="masculino")

        if "cítrico" in query:
            queryset = queryset.filter(flavor="cítrico")
        elif "amadeirado" in query:
            queryset = queryset.filter(flavor="amadeirado")

        if target:
            queryset = queryset.filter(target=target)

        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)