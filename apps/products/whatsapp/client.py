import requests

WHATSAPP_TOKEN = "EAAXyR3yUZCKEBRJw447aP42TuucBZAwQNifK5Ol7N525Uehb0PWIf1mjDXZC67DeAaxghtoX8eaYWtb5iflmBgvMJszkAxZAj5kHA9gYMEZCyCSTq4ZBCh2ZCm83t2MDSTpwYJ5Gp5sdno5n1XqZAg069Y5W2COSNeEWABGEJOCBIruLZA8v8ZCPZAHZBNZBgV0gKG7SpT4my7nkQpPzAaNdjf7NMWZBJrgP6EgDP5CJUaddugYD8qPjmja3EkjIlZA3gA22sEi5EUvlJaFFcZA5EDz4tm8Y27acuFrE8nZBLdbw6fQZDZD"
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