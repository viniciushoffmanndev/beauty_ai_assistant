from .product_search_service import ProductSearchService
from .product_context_service import ProductContextService
from .user_selection_service import UserSelectionService
from .product_recommendation_service import ProductRecommendationService

product_context_service = ProductContextService()

product_search_service = ProductSearchService(
    context_service=product_context_service
)

product_recommendation_service = ProductRecommendationService(
    search_service=product_search_service,
    context_service=product_context_service,
)


def search_products_in_es(query: str, size: int = 5) -> list[dict]:
    return product_search_service.search(query, size=size)


def buscar_produto_por_id(product_id: str) -> dict | None:
    return product_search_service.get_product_by_id(product_id)


def salvar_escolha_usuario(user_id: str, product_id: str) -> None:
    UserSelectionService.save_selection(user_id, product_id)