import json
from bs4 import BeautifulSoup
import requests
from .validators import validate_product


def get_text(el):
    return  el.text.strip() if el else None

def get_attr(el, attr):
    return el.get(attr) if el and el.has_attr(attr) else None

def get_price(text):
    if not text:
        return None
    try:
        return float(text.replace("R$", "").replace(",", "."))
    except:
        return None

def parse_product(item):
    
    nome = get_text("span", class_="showcase-item-title").text.strip()
    marca = get_text("span", class_="showcase-item-brand").text.strip()

    preco = get_price("span", class_="price-value").text.strip()
    preco = float(preco.replace("R$", "").replace(",", "."))

    preco_antigo = get_price("div", class_="item-price-max")
    preco_antigo = float(preco_antigo.text.replace("R$", "").replace(",", ".")) if preco_antigo else None

    desconto = get_text("span", class_="item-discount")
    desconto = int(desconto.text.replace("-", "").replace("%", "").strip()) if desconto else None

    descricao = get_text("p", class_="showcase-item-description").text.strip()

    link = get_attr("a", class_="showcase-item-name")["href"]
    imagem = get_attr("img")["src"]

    rating_div = get_text("div", class_="showcase-item-rating")
    rating = None
    reviews = None

    if rating_div:
        aria = rating_div.get("aria-label", "")
        if "Nota" in aria:
            rating = float(aria.split(" ")[1])
        if "avaliações" in rating_div.get("title", ""):
            reviews = int(rating_div["title"].split(" ")[0])

    raw = json.loads(item["data-event"].replace("&quot;", '"'))

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

def scrape_products(url):
    headers = {"User-Agent": "Mozilla/5.0"}
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