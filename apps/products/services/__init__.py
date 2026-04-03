from apps.products.services.product_search_service import ProductSearchService
from apps.products.services.user_selection_service import UserSelectionService


_search_service = ProductSearchService()
_selection_service = UserSelectionService()


def search_products_in_es(query: str, size: int = 5) -> list[dict]:
    return _search_service.search(query=query, size=size)


def buscar_produto_por_id(product_id: str) -> dict | None:
    return _search_service.get_product_by_external_id(product_id)


def salvar_escolha_usuario(user_id: str, product_id: str) -> None:
    _selection_service.save_selection(user_id=user_id, product_id=product_id)
