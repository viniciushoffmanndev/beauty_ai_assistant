import requests
import os
from django.conf import settings
import json
from apps.products.models import Product
import unicodedata



WHATSAPP_TOKEN = settings.WHATSAPP_TOKEN
PHONE_NUMBER_ID = settings.PHONE_NUMBER_ID


def send_whatsapp_request(payload):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        print("Status:", response.status_code)
        print("Resposta:", response.text)
    except requests.exceptions.RequestException as e:
        print("Erro ao enviar requisição:", e)

def send_whatsapp_message(to, text):
    if not to or not text:
        print("Erro: número ou texto inválido")
        return

    payload = {
        "messaging_product": "whatsapp",
        "to": str(to).strip(),  # garante que é string limpa
        "type": "text",
        "text": {"body": text[:1024]}  # corta se for muito longo
    }

    print("Payload enviado:", json.dumps(payload, indent=2, ensure_ascii=False))  # debug
    send_whatsapp_request(payload)

def send_whatsapp_image(to, image_url, caption):
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "image",
        "image": {"link": image_url, "caption": caption}
    }
    send_whatsapp_request(payload)


def send_whatsapp_buttons(to, text, buttons):
    payload = {
        "messaging_product": "whatsapp",
        "to": str(to).strip(),
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {"text": text[:1024]},
            "action": {
                "buttons": [
                    {"type": "reply", "reply": {"id": f"btn_{i}", "title": b[:20]}}
                    for i, b in enumerate(buttons, start=1)
                ]
            }
        }
    }
    send_whatsapp_request(payload)

def send_whatsapp_cta(to, text, button_text, url_link):
    payload = {
        "messaging_product": "whatsapp",
        "to": str(to).strip(),
        "type": "interactive",
        "interactive": {
            "type": "cta_url",
            "body": {"text": text[:1024]},
            "action": {
                "name": "cta_url",
                "parameters": {
                    "display_text": button_text[:20],
                    "url": url_link
                }
            }
        }
    }
    send_whatsapp_request(payload)

def normalize_text(text, max_len):
    # Remove acentos e caracteres especiais
    text = unicodedata.normalize("NFKD", text).encode("ASCII", "ignore").decode("ASCII")
    return text[:max_len]


# cache global para mapear IDs da lista aos produtos
produtos_cache = {}

def send_whatsapp_list(to, produtos):
    global produtos_cache
    produtos_cache = {f"produto_{idx}": r for idx, r in enumerate(produtos, start=1)}

    rows = []
    for idx, r in enumerate(produtos, start=1):
        name = normalize_text(str(r.get("name") or "Produto"), 20)  # título ≤ 20
        price = r.get("price")
        description_raw = str(r.get("description") or "")
        description = normalize_text(description_raw, 60)  # corta base para caber junto com preço
        price_info = f"R$ {price:.2f}" if isinstance(price, (int, float)) else "Preço indisponível"

        full_description = f"{price_info} - {description}"
        full_description = full_description[:72]  # garante ≤72 no final

        rows.append({
            "id": f"produto_{idx}",
            "title": name,
            "description": full_description
        })

    payload = {
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
                "sections": [{"title": "Promoções", "rows": rows}]
            }
        }
    }

    for row in rows:
        print(f"ID={row['id']} | title='{row['title']}' ({len(row['title'])}) | description length={len(row['description'])}")

    print("Payload enviado:", json.dumps(payload, indent=2, ensure_ascii=False))
    send_whatsapp_request(payload)


def buscar_produto_por_id(selected_id):
    global produtos_cache
    return produtos_cache.get(selected_id)
