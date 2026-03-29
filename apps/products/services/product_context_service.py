import logging

logger = logging.getLogger(__name__)


class ProductContextService:
    def __init__(self):
        self._cache: dict[str, dict] = {}

    def save_products(self, products: list[dict]) -> None:
        for product in products:
            product_id = product.get("_id")
            if product_id:
                self._cache[product_id] = product

    def get_product_by_id(self, product_id: str) -> dict | None:
        return self._cache.get(product_id)

    def clear(self) -> None:
        self._cache.clear()
        logger.info("Cache de contexto de produtos limpo")