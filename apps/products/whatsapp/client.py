import requests

WHATSAPP_TOKEN = "EAAXyR3yUZCKEBRIKqcY5FMJVZAR8j82149LPDaHu9ClsGtiWCXUX3bjZAV4inbfWCgtDqZAdUi2jTFhgwZCJjXgshGUyQcuTWA8qg9CqHjWm8ThoyE7nxOChd4rYSbZBpHEDzfgXKkwzxBfcZCb9ZBVXC9ieiL3TCQ0r7Xz8FlLtjwBtf79Omp40jsvbakuuqOojV7HnT5P6YK0MXk9ydt8ZBwhz8imXoTZCuC86abF8xdskwZCotQ6Pst5ngHbXEumlI2coVsd611vYX2Kyb76BEZBQ5dAnzznI2y0c0mw1zAZDZD"
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