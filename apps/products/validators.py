def validate_product(product: dict) -> None:
    if not product.get("name"):
        raise ValueError("Produto sem nome")

    if not product.get("url"):
        raise ValueError("Produto sem URL")