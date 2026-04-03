from apps.products.utils.formatters import format_brl
from apps.products.utils.text import normalize_text


class WhatsAppMessageBuilder:
    @staticmethod
    def build_product_details(product: dict) -> str:
        name = product.get("name", "Produto")
        brand = product.get("brand") or "Marca não informada"
        description = product.get("description") or "Sem descrição disponível"
        price_text = format_brl(product.get("price"))

        message = (
            f"*{name}*\n"
            f"Marca: {brand}\n"
            f"Preço: {price_text}\n\n"
            f"{description}\n\n"
        )

        if product.get("url"):
            message += f"Comprar: {product['url']}"

        return message

    @staticmethod
    def build_list_row(product: dict) -> dict | None:
        external_id = str(product.get("external_id") or "").strip()
        if not external_id:
            return None

        name = normalize_text(str(product.get("name") or "Produto"), 20)
        description = normalize_text(str(product.get("description") or ""), 60)
        price_info = format_brl(product.get("price"))
        full_description = f"{price_info} - {description}"[:72]

        return {
            "id": external_id,
            "title": name,
            "description": full_description,
        }

    @classmethod
    def build_list_rows(cls, products: list[dict]) -> list[dict]:
        rows = []

        for product in products[:5]:
            row = cls.build_list_row(product)
            if row:
                rows.append(row)

        return rows

    @staticmethod
    def build_list_payload(to: str, rows: list[dict]) -> dict:
        return {
            "messaging_product": "whatsapp",
            "to": str(to).strip(),
            "type": "interactive",
            "interactive": {
                "type": "list",
                "header": {"type": "text", "text": "Perfumes disponíveis"},
                "body": {"text": "Escolha um perfume para ver mais detalhes:"},
                "footer": {"text": "Beauty AI Assistant"},
                "action": {
                    "button": "Ver opções",
                    "sections": [{"title": "Promoções", "rows": rows}],
                },
            },
        }

    # aliases de compatibilidade (opcional, mas útil)
    build_product_details_message = build_product_details


# aliases funcionais para manter compatibilidade fora da classe também
build_product_details = WhatsAppMessageBuilder.build_product_details
build_product_details_message = WhatsAppMessageBuilder.build_product_details
build_list_row = WhatsAppMessageBuilder.build_list_row
build_list_rows = WhatsAppMessageBuilder.build_list_rows
build_list_payload = WhatsAppMessageBuilder.build_list_payload