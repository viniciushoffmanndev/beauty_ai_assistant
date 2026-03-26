import requests

WHATSAPP_TOKEN = "EAAXyR3yUZCKEBRIW3borJbIo6uJmI3eeMbgQE2ihAb5Fw99jonjXzl6ZBuinxNGbtcg87T4PlZAaZAVuZC3KpBDieA3G7mKTt4trUSWTMltKDhVq4sCPZAZB4MUsBm4h2iLOlqGSTHpnVOoHoaNWvog9T1bSa7pvlEp3RX2ZBovfl8x6Y0xieGx52jwVJPHpRdrNiE0NYk6mZBSP8sUCL6jW8ClRwuitbRtfTmCBNvPBLQXukrttNSDZC8BUOKbWBZBXgkQblK0RtQPH6tE7SqmsHOA7ZCc6MnODVqWbR1tPTwZDZD"
PHONE_NUMBER_ID = "1105730849281197"


def send_whatsapp_image(to, image_url, caption):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "image",
        "image": {
            "link": image_url,
            "caption": caption
        }
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        print("Status:", response.status_code)
        print("Resposta:", response.text)
    except requests.exceptions.RequestException as e:
        print("Erro ao enviar imagem:", e)


def send_whatsapp_message(to, text):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {
            "body": text
        }
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        print("Status:", response.status_code)
        print("Resposta:", response.text)
    except requests.exceptions.RequestException as e:
        print("Erro ao enviar mensagem:", e)

def send_whatsapp_cta(to, text, button_text, url_link):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "cta_url",
            "body": {
                "text": text
            },
            "action": {
                "name": "cta_url",
                "parameters": {
                    "display_text": button_text,
                    "url": url_link
                }
            }
        }
    }

    response = requests.post(url, json=payload, headers=headers)

    print("Status:", response.status_code)
    print("Resposta:", response.text)