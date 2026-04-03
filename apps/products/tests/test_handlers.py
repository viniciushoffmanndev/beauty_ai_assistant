from unittest.mock import patch

from django.test import SimpleTestCase

from apps.products.whatsapp.handlers import (
    handle_button_reply,
    handle_list_reply,
    handle_text_message,
)


class WhatsAppHandlersTest(SimpleTestCase):
    @patch("apps.products.whatsapp.handlers.send_whatsapp_text")
    def test_handle_text_message_deve_responder_quando_query_vazia(self, mock_send):
        handle_text_message("5511999999999", "   ")

        mock_send.assert_called_once()
        self.assertIn("Digite o nome de um perfume", mock_send.call_args[0][1])

    @patch("apps.products.whatsapp.handlers.send_whatsapp_text")
    @patch("apps.products.whatsapp.handlers.search_service.search")
    def test_handle_text_message_deve_responder_sem_resultados(self, mock_search, mock_send):
        mock_search.return_value = []

        handle_text_message("5511999999999", "malbec")

        mock_search.assert_called_once_with(query="malbec", size=5)
        mock_send.assert_called_once()
        self.assertIn("Não encontrei produtos", mock_send.call_args[0][1])

    @patch("apps.products.whatsapp.handlers.send_whatsapp_list")
    @patch("apps.products.whatsapp.handlers.search_service.search")
    def test_handle_text_message_deve_enviar_lista(self, mock_search, mock_list):
        mock_search.return_value = [
            {"external_id": "SKU123", "name": "Malbec"}
        ]

        handle_text_message("5511999999999", "malbec")

        mock_search.assert_called_once_with(query="malbec", size=5)
        mock_list.assert_called_once()

    @patch("apps.products.whatsapp.handlers.send_whatsapp_text")
    @patch("apps.products.whatsapp.handlers.search_service.get_product_by_external_id")
    @patch("apps.products.whatsapp.handlers.selection_service.save_selection")
    def test_handle_list_reply_deve_enviar_detalhes(
        self,
        mock_save_selection,
        mock_get_product,
        mock_send,
    ):
        mock_get_product.return_value = {
            "external_id": "SKU123",
            "name": "Malbec",
            "brand": "O Boticário",
            "description": "Perfume amadeirado",
            "price": 199.90,
            "url": "https://example.com/produto",
        }

        handle_list_reply(
            to="5511999999999",
            user_id="5511999999999",
            product_id="SKU123",
        )

        mock_save_selection.assert_called_once_with("5511999999999", "SKU123")
        mock_get_product.assert_called_once_with("SKU123")
        mock_send.assert_called_once()
        self.assertIn("*Malbec*", mock_send.call_args[0][1])

    @patch("apps.products.whatsapp.handlers.send_whatsapp_text")
    @patch("apps.products.whatsapp.handlers.search_service.get_product_by_external_id")
    @patch("apps.products.whatsapp.handlers.selection_service.save_selection")
    def test_handle_list_reply_deve_responder_quando_produto_nao_existe(
        self,
        mock_save_selection,
        mock_get_product,
        mock_send,
    ):
        mock_get_product.return_value = None

        handle_list_reply(
            to="5511999999999",
            user_id="5511999999999",
            product_id="SKU999",
        )

        mock_save_selection.assert_called_once_with("5511999999999", "SKU999")
        mock_send.assert_called_once()
        self.assertIn("Produto não encontrado", mock_send.call_args[0][1])

    @patch("apps.products.whatsapp.handlers.send_whatsapp_text")
    def test_handle_button_reply(self, mock_send):
        handle_button_reply("5511999999999", "SKU123", "buy")

        mock_send.assert_called_once()
        self.assertIn("buy", mock_send.call_args[0][1])
        self.assertIn("SKU123", mock_send.call_args[0][1])
