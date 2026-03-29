from apps.products.services import (
    product_recommendation_service,
    salvar_escolha_usuario,
)
from apps.products.whatsapp.client import (
    send_whatsapp_cta,
    send_whatsapp_image,
    send_whatsapp_message,
    send_whatsapp_buttons,
    send_whatsapp_list,
)


def handle_text_message(to: str, query: str) -> None:
    results = product_recommendation_service.recommend_products(query, size=5)

    if not results:
        send_whatsapp_message(
            to,
            product_recommendation_service.build_no_results_message()
        )
        return

    send_whatsapp_list(to, results)


def handle_list_reply(to: str, user_id: str, product_id: str) -> None:
    product = product_recommendation_service.get_product_details(product_id)

    if not product:
        send_whatsapp_message(to, "Produto não encontrado.")
        return

    salvar_escolha_usuario(user_id, product_id)

    caption = product_recommendation_service.build_product_caption(product)

    if product.get("image"):
        send_whatsapp_image(
            to,
            product["image"],
            caption
        )
    else:
        send_whatsapp_message(to, caption)

    send_whatsapp_buttons(
        to,
        "O que deseja fazer?",
        [
            {"id": f"buy_now|{product_id}", "title": "Comprar agora"},
            {"id": f"view_description|{product_id}", "title": "Ver descrição"},
            {"id": f"talk_to_agent|{product_id}", "title": "Atendente"},
        ]
    )


def handle_button_reply(to: str, product_id: str, button_id: str) -> None:
    product = product_recommendation_service.get_product_details(product_id)

    if not product:
        send_whatsapp_message(to, "Produto não encontrado.")
        return

    if button_id == "buy_now":
        send_whatsapp_cta(
            to,
            f"Confira {product.get('name', 'este produto')} no site:",
            "Comprar agora",
            product.get("url", "https://www.boticario.com.br/")
        )

    elif button_id == "view_description":
        send_whatsapp_message(
            to,
            product_recommendation_service.build_description_message(product)
        )

    elif button_id == "talk_to_agent":
        send_whatsapp_message(
            to,
            "Um atendente irá falar com você em instantes."
        )

    else:
        send_whatsapp_message(
            to,
            "Não entendi sua escolha. Tente novamente."
        )