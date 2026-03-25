from apps.products.services import search_products_in_es
from .client import send_whatsapp_image, send_whatsapp_message, send_whatsapp_cta

def handle_whatsapp_message(to, query):
    results = search_products_in_es(query, size=3)

    if not results:
        send_whatsapp_message(
            to,
            "Não encontrei produtos para sua busca. Deseja tentar outra categoria?"
        )
        return

    for r in results:
        name = r.get("name") or "Produto"
        brand = r.get("brand") or ""
        price = r.get("price")
        old_price = r.get("old_price")
        discount = r.get("discount")
        rating = r.get("rating")
        review_count = r.get("review_count")
        description = r.get("description")
        image = r.get("image")
        url = r.get("url")

        # preço
        if price is not None:
            if old_price is not None and discount is not None:
                price_info = f"De R$ {old_price:.2f} por R$ {price:.2f} (-{discount}%)"
            else:
                price_info = f"R$ {price:.2f}"
        else:
            price_info = "Preço indisponível"

        # avaliação
        if rating is not None and review_count is not None:
            rating_info = f"{rating:.1f} ({review_count} avaliações)"
        else:
            rating_info = ""

        # legenda
        caption = f"*{name}*"
        if brand:
            caption += f" ({brand})"

        caption += f"\n{price_info}"

        if rating_info:
            caption += f"\n{rating_info}"

        if description:
            caption += f"\n{description[:80]}..."

        if url:
            caption += f"\n\n{url}"

        # envio
        if url:
            send_whatsapp_cta(
                to,
                caption,
                "Comprar agora",
                url
            )
        elif image:
            send_whatsapp_image(to, image, caption)
        else:
            send_whatsapp_message(to, caption)
        