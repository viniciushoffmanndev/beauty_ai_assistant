def format_brl(value) -> str:
    if value is None:
        return "Preço indisponível"

    try:
        return f"R$ {float(value):.2f}"
    except (TypeError, ValueError):
        return "Preço indisponível"
