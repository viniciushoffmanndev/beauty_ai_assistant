from apps.products.parsers.whatsapp_webhook_parser import WhatsAppWebhookParser
from apps.products.whatsapp.handlers import (
    handle_text_message,
    handle_list_reply,
    handle_button_reply,
)


class WhatsAppWebhookService:
    @staticmethod
    def process(payload: dict) -> None:
        entry = WhatsAppWebhookParser.extract_entry(payload)
        messages = WhatsAppWebhookParser.extract_messages(entry)

        if not messages:
            return

        contact_wa_id = WhatsAppWebhookParser.extract_contact_wa_id(entry)

        for message in messages:
            message_type = WhatsAppWebhookParser.extract_message_type(message)
            sender = WhatsAppWebhookParser.extract_sender(message)

            if not sender:
                continue

            if message_type == "text":
                text_body = WhatsAppWebhookParser.extract_text_body(message)

                if text_body:
                    handle_text_message(sender, text_body)

            elif message_type == "interactive":
                interactive_type = WhatsAppWebhookParser.extract_interactive_type(message)

                if interactive_type == "list_reply":
                    selected_id = WhatsAppWebhookParser.extract_list_reply_id(message)

                    if selected_id:
                        handle_list_reply(
                            to=sender,
                            user_id=contact_wa_id or sender,
                            product_id=selected_id,
                        )

                elif interactive_type == "button_reply":
                    button_id = WhatsAppWebhookParser.extract_button_reply_id(message)

                    if button_id:
                        # Espera formato: action|product_id
                        parts = button_id.split("|")

                        if len(parts) == 2:
                            action, product_id = parts
                            handle_button_reply(
                                to=sender,
                                product_id=product_id,
                                button_id=action,
                            )