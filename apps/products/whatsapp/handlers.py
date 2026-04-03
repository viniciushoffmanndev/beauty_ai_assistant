from apps.products.services.product_search_service import ProductSearchService
from apps.products.services.user_selection_service import UserSelectionService
from apps.products.whatsapp.client import send_whatsapp_list, send_whatsapp_text
from apps.products.whatsapp.message_builder import WhatsAppMessageBuilder

search_service = ProductSearchService()
selection_service = UserSelectionService()


def handle_text_message(to: str, text: str) -> None:
    query = text.strip()

    if not query:
        send_whatsapp_text(
            to,
            "Digite o nome de um perfume, marca ou categoria para buscar produtos.",
        )
        return

    products = search_service.search(query=query, size=5)

    if not products:
        send_whatsapp_text(
            to,
            "Não encontrei produtos para sua busca. Tente pesquisar por categoria, fragrância ou marca.",
        )
        return

    send_whatsapp_list(to, products)


def handle_list_reply(to: str, user_id: str, product_id: str) -> None:
    selection_service.save_selection(user_id, product_id)

    product = search_service.get_product_by_external_id(product_id)

    if not product:
        send_whatsapp_text(to, "Produto não encontrado.")
        return

    message = WhatsAppMessageBuilder.build_product_details_message(product)
    send_whatsapp_text(to, message)


def handle_button_reply(to: str, product_id: str, button_id: str) -> None:
    send_whatsapp_text(to, f"Ação recebida: {button_id} para o produto {product_id}")