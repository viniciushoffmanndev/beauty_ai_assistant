from typing import Any


class WhatsAppWebhookParser:
    @staticmethod
    def extract_entry(data: dict[str, Any]) -> dict[str, Any]:
        return data.get("entry", [{}])[0].get("changes", [{}])[0].get("value", {})

    @staticmethod
    def extract_messages(entry: dict[str, Any]) -> list[dict[str, Any]]:
        return entry.get("messages", [])

    @staticmethod
    def extract_contact_wa_id(entry: dict[str, Any]) -> str | None:
        contacts = entry.get("contacts", [])
        if not contacts:
            return None
        return contacts[0].get("wa_id")

    @staticmethod
    def extract_message_type(message: dict[str, Any]) -> str | None:
        return message.get("type")

    @staticmethod
    def extract_sender(message: dict[str, Any]) -> str | None:
        return message.get("from")

    @staticmethod
    def extract_text_body(message: dict[str, Any]) -> str | None:
        return message.get("text", {}).get("body")

    @staticmethod
    def extract_list_reply_id(message: dict[str, Any]) -> str | None:
        return message.get("interactive", {}).get("list_reply", {}).get("id")

    @staticmethod
    def extract_list_reply_title(message: dict[str, Any]) -> str | None:
        return message.get("interactive", {}).get("list_reply", {}).get("title")

    @staticmethod
    def extract_button_reply_id(message: dict[str, Any]) -> str | None:
        return message.get("interactive", {}).get("button_reply", {}).get("id")

    @staticmethod
    def extract_button_reply_title(message: dict[str, Any]) -> str | None:
        return message.get("interactive", {}).get("button_reply", {}).get("title")

    @staticmethod
    def extract_interactive_type(message: dict[str, Any]) -> str | None:
        return message.get("interactive", {}).get("type")
