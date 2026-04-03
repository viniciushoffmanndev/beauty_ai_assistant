from django.test import SimpleTestCase

from apps.products.parsers.whatsapp_webhook_parser import WhatsAppWebhookParser


class WhatsAppWebhookParserTest(SimpleTestCase):
    def setUp(self):
        self.payload = {
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

    def test_extract_entry(self):
        entry = WhatsAppWebhookParser.extract_entry(self.payload)
        self.assertIn("messages", entry)

    def test_extract_messages(self):
        entry = WhatsAppWebhookParser.extract_entry(self.payload)
        messages = WhatsAppWebhookParser.extract_messages(entry)
        self.assertEqual(len(messages), 1)

    def test_extract_contact_wa_id(self):
        entry = WhatsAppWebhookParser.extract_entry(self.payload)
        wa_id = WhatsAppWebhookParser.extract_contact_wa_id(entry)
        self.assertEqual(wa_id, "5511999999999")

    def test_extract_text_body(self):
        entry = WhatsAppWebhookParser.extract_entry(self.payload)
        message = WhatsAppWebhookParser.extract_messages(entry)[0]
        self.assertEqual(
            WhatsAppWebhookParser.extract_text_body(message),
            "Malbec",
        )

    def test_extract_interactive_list_reply_id(self):
        message = {
            "interactive": {
                "type": "list_reply",
                "list_reply": {
                    "id": "SKU123",
                    "title": "Produto X",
                }
            }
        }
        self.assertEqual(
            WhatsAppWebhookParser.extract_interactive_type(message),
            "list_reply",
        )
        self.assertEqual(
            WhatsAppWebhookParser.extract_list_reply_id(message),
            "SKU123",
        )
        self.assertEqual(
            WhatsAppWebhookParser.extract_list_reply_title(message),
            "Produto X",
        )

    def test_extract_interactive_button_reply(self):
        message = {
            "interactive": {
                "type": "button_reply",
                "button_reply": {
                    "id": "buy|SKU123",
                    "title": "Comprar",
                }
            }
        }
        self.assertEqual(
            WhatsAppWebhookParser.extract_button_reply_id(message),
            "buy|SKU123",
        )
        self.assertEqual(
            WhatsAppWebhookParser.extract_button_reply_title(message),
            "Comprar",
        )
