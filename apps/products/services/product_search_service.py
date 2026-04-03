import logging

from elasticsearch_dsl import Q, Search

from apps.products.es_client import es
from apps.products.services.query_filter_service import QueryFilterService

logger = logging.getLogger(__name__)


class ProductSearchService:
    def __init__(self, filter_service: QueryFilterService | None = None):
        self.filter_service = filter_service or QueryFilterService()

    def search(self, query: str, size: int = 5) -> list[dict]:
        filters = self.filter_service.extract_filters(query)
        clean_query = self.filter_service.clean_query(query) or query

        q = Q(
            "multi_match",
            query=clean_query,
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

        logger.info(
            "Busca executada com sucesso | query=%s | clean_query=%s | filtros=%s | resultados=%s",
            query,
            clean_query,
            filters,
            len(results),
        )
        return results

    def get_product_by_external_id(self, external_id: str) -> dict | None:
        try:
            search = Search(using=es, index="products").query(
                "term",
                external_id=external_id,
            )[:1]

            response = search.execute()

            if not response.hits:
                logger.warning(
                    "Produto não encontrado por external_id | external_id=%s",
                    external_id,
                )
                return None

            hit = response.hits[0]
            doc = hit.to_dict()
            doc["_id"] = hit.meta.id

            logger.info(
                "Produto encontrado por external_id | external_id=%s | name=%s",
                external_id,
                doc.get("name"),
            )
            return doc

        except Exception as exc:
            logger.exception(
                "Erro ao buscar produto por external_id | external_id=%s | erro=%s",
                external_id,
                exc,
            )
            return None
