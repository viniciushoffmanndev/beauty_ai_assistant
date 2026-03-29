from typing import Optional


class ProductRecommendationService:
    def __init__(self, search_service, context_service):
        self.search_service = search_service
        self.context_service = context_service

    def recommend_products(self, query: str, size: int = 5) -> list[dict]:
        if not query:
            return []

        return self.search_service.search(query=query, size=size)

    def get_product_details(self, product_id: str) -> Optional[dict]:
        if not product_id:
            return None

        return self.search_service.get_product_by_id(product_id)

    def build_no_results_message(self) -> str:
        return (
            "Não encontrei produtos para sua busca. "
            "Tente pesquisar por categoria, fragrância ou marca."
        )

    def build_product_caption(self, product: dict) -> str:
        name = product.get("name", "Produto")
        price = product.get("price")

        if price is not None:
            try:
                return f"{name} - R$ {float(price):.2f}"
            except (TypeError, ValueError):
                pass

        return name

    def build_description_message(self, product: dict) -> str:
        name = product.get("name", "Produto")
        description = product.get("description") or "Sem descrição disponível."
        return f"{name}\n\n{description}"