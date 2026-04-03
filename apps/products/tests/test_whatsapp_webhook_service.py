from unittest.mock import patch

from django.test import SimpleTestCase

from apps.products.services.whatsapp_webhook_service import WhatsAppWebhookService


class WhatsAppWebhookServiceTest(SimpleTestCase):
    @patch("apps.products.services.whatsapp_webhook_service.handle_text_message")
    def test_process_deve_tratar_mensagem_texto(self, mock_handle_text):
        payload = {
            "entry": [
                {
                    "changes": [
                        {
                            "value": {
                                "contacts": [{"wa_id": "5511999999999"}],
                                "messages": [
                                    {
                                        "from": "5511999999999",
                                        "type": "text",
                                        "text": {"body": "Malbec"},
                                    }
                                ],
                            }
                        }
                    ]
                }
            ]
        }

        WhatsAppWebhookService.process(payload)

        mock_handle_text.assert_called_once_with("5511999999999", "Malbec")

    @patch("apps.products.services.whatsapp_webhook_service.handle_list_reply")
    def test_process_deve_tratar_list_reply(self, mock_handle_list_reply):
        payload = {
            "entry": [
                {
                    "changes": [
                        {
                            "value": {
                                "contacts": [{"wa_id": "5511999999999"}],
                                "messages": [
                                    {
                                        "from": "5511888888888",
                                        "type": "interactive",
                                        "interactive": {
                                            "type": "list_reply",
                                            "list_reply": {
                                                "id": "SKU123",
                                                "title": "Malbec"
                                            }
                                        },
                                    }
                                ],
                            }
                        }
                    ]
                }
            ]
        }

        WhatsAppWebhookService.process(payload)

        mock_handle_list_reply.assert_called_once_with(
            to="5511888888888",
            user_id="5511999999999",
            product_id="SKU123",
        )

    @patch("apps.products.services.whatsapp_webhook_service.handle_button_reply")
    def test_process_deve_tratar_button_reply(self, mock_handle_button_reply):
        payload = {
            "entry": [
                {
                    "changes": [
                        {
                            "value": {
                                "contacts": [{"wa_id": "5511999999999"}],
                                "messages": [
                                    {
                                        "from": "5511888888888",
                                        "type": "interactive",
                                        "interactive": {
                                            "type": "button_reply",
                                            "button_reply": {
                                                "id": "buy|SKU123",
                                                "title": "Comprar"
                                            }
                                        },
                                    }
                                ],
                            }
                        }
                    ]
                }
            ]
        }

        WhatsAppWebhookService.process(payload)

        mock_handle_button_reply.assert_called_once_with(
            to="5511888888888",
            product_id="SKU123",
            button_id="buy",
        )

    def test_process_nao_deve_quebrar_sem_messages(self):
        payload = {
            "entry": [
                {
                    "changes": [
                        {
                            "value": {}
                        }
                    ]
                }
            ]
        }

        WhatsAppWebhookService.process(payload)
