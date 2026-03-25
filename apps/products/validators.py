REQUIRED_FIELDS = ["external_id", "name", "price", "url"]


def validate_product(data):
    errors = []

    for field in REQUIRED_FIELDS:
        if not data.get(field):
            errors.append(f"Campo obrigatório ausente: {field}")

    # validações específicas
    if data.get("price") is not None:
        if data["price"] <= 0:
            errors.append("Preço inválido (<= 0)")

    if data.get("rating") is not None:
        if not (0 <= data["rating"] <= 5):
            errors.append("Rating fora do intervalo (0-5)")

    if data.get("discount") is not None:
        if not (0 <= data["discount"] <= 100):
            errors.append("Desconto inválido")

    if errors:
        raise ValueError(" | ".join(errors))

    return True