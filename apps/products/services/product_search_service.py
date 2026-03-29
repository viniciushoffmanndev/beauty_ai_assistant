import logging

from elasticsearch_dsl import Q, Search

from apps.products.es_client import es
from apps.products.services.query_filter_service import QueryFilterService
from apps.products.services.product_context_service import ProductContextService

logger = logging.getLogger(__name__)


class ProductSearchService:
    def __init__(
        self,
        filter_service: QueryFilterService | None = None,
        context_service: ProductContextService | None = None,
    ):
        self.filter_service = filter_service or QueryFilterService()
        self.context_service = context_service or ProductContextService()

    def search(self, query: str, size: int = 5) -> list[dict]:
        filters = self.filter_service.extract_filters(query)

        q = Q(
            "multi_match",
            query=query,
            fields=[
                "name^3",
                "description",
                "brand",
                "flavor",
                "target",
                "category",
            ],
            fuzziness="AUTO",
        )

        search = Search(using=es, index="products").query(q).filter(
            "term", is_active=True
        )

        for field, value in filters:
            search = search.filter("term", **{field: value})

        response = search[:size].execute()

        results = []
        for hit in response:
            doc = hit.to_dict()
            doc["_id"] = hit.meta.id
            results.append(doc)

        self.context_service.save_products(results)

        logger.info(
            "Busca executada com sucesso | query=%s | resultados=%s",
            query,
            len(results),
        )

        return results

    def get_product_by_id(self, product_id: str) -> dict | None:
        return self.context_service.get_product_by_id(product_id)