import json
import logging

import requests
from django.conf import settings

from apps.products.whatsapp.message_builder import build_list_payload, build_list_rows

logger = logging.getLogger(__name__)


def send_whatsapp_request(payload: dict) -> None:
    url = f"https://graph.facebook.com/v18.0/{settings.PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }

    response = requests.post(url, headers=headers, json=payload, timeout=15)

    logger.info("Payload enviado ao WhatsApp: %s", json.dumps(payload, ensure_ascii=False))
    logger.info("Resposta WhatsApp | status=%s | body=%s", response.status_code, response.text)

    response.raise_for_status()


def send_whatsapp_text(to: str, message: str) -> None:
    payload = {
        "messaging_product": "whatsapp",
        "to": str(to).strip(),
        "type": "text",
        "text": {"body": message},
    }
    send_whatsapp_request(payload)


def send_whatsapp_list(to: str, products: list[dict]) -> None:
    rows = build_list_rows(products)

    if not rows:
        send_whatsapp_text(
            to,
            "Não encontrei produtos válidos para exibir no momento.",
        )
        return

    payload = build_list_payload(to, rows)
    send_whatsapp_request(payload)
