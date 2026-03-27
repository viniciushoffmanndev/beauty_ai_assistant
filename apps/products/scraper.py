import json
from bs4 import BeautifulSoup
import requests
from .validators import validate_product


def get_text(parent, tag, **kwargs):
    el = parent.find(tag, **kwargs)
    return el.text.strip() if el else None

def get_attr(parent, tag, **kwargs):
    el = parent.find(tag, **kwargs)
    return el.attrs if el else {}

def get_price(parent, tag, **kwargs):
    el = parent.find(tag, **kwargs)
    return el.text.strip() if el else None

def parse_product(item):
    nome = get_text(item, "span", class_="showcase-item-title")
    marca = get_text(item, "span", class_="showcase-item-brand")

    preco = get_price(item, "span", class_="price-value")
    preco = float(preco.replace("R$", "").replace(",", ".")) if preco else None

    preco_antigo = get_price(item, "div", class_="item-price-max")
    preco_antigo = float(preco_antigo.replace("R$", "").replace(",", ".")) if preco_antigo else None

    desconto = get_text(item, "span", class_="item-discount")
    desconto = int(desconto.replace("-", "").replace("%", "").strip()) if desconto else None

    descricao = get_text(item, "p", class_="showcase-item-description")

    link = get_attr(item, "a", class_="showcase-item-name").get("href")
    attrs = get_attr(item, "img")
    imagem = attrs.get("data-src") or attrs.get("data-original") or attrs.get("src")

    rating_div = item.find("div", class_="showcase-item-rating")
    rating = None
    reviews = None

    if rating_div:
        aria = rating_div.get("aria-label", "")
        if "Nota" in aria:
            rating = float(aria.split(" ")[1])
        if "avaliações" in rating_div.get("title", ""):
            reviews = int(rating_div["title"].split(" ")[0])

    raw = json.loads(item.get("data-event", "").replace("&quot;", '"'))

    return {
        "external_id": raw.get("sku"),
        "source": "boticario",
        "name": nome,
        "brand": marca,
        "price": preco,
        "old_price": preco_antigo,
        "discount": desconto,
        "rating": rating,
        "review_count": reviews,
        "description": descricao,
        "url": link,
        "image": imagem,
    }

def scrapping(url):

    headers = {
    "User-Agent": (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "Version/18.5 Mobile/15E148 Safari/604.1"
    ),
    "Accept": "application/json",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    }

    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code != 200:
        raise Exception(f"Erro ao acessar {url}")

    soup = BeautifulSoup(response.text, "html.parser")

    artigos = soup.find_all("article")

    if not artigos:
        raise Exception(" Nenhum produto encontrado — possível mudança no site")

    produtos = []
    erros = 0

    for item in artigos:
        try:
            data = parse_product(item)

            # VALIDAÇÃO AQUI
            validate_product(data)

            produtos.append(data)

        except Exception as e:
            erros += 1
            print("Erro ao processar produto:", e)

    # validação global
    if len(produtos) < 5:
        raise Exception(f"Poucos produtos válidos: {len(produtos)}")

    print(f" Produtos válidos: {len(produtos)} | Erros: {erros}")

    return produtos