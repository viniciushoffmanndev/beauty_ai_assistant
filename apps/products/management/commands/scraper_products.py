from django.core.management.base import BaseCommand
from elasticsearch import Elasticsearch
from apps.products.scraper import scrapping
from apps.products.models import Product
from datetime import datetime
import hashlib

def gerar_external_id(produto):
    """
    Gera um external_id único.
    Se já existir no produto, usa ele.
    Caso contrário, gera um hash da URL.
    """
    if produto.get("external_id"):
        return produto["external_id"]
    else:
        return hashlib.md5(produto["url"].encode()).hexdigest()

class Command(BaseCommand):
    help = "Roda o scraper e salva/atualiza os produtos no Elasticsearch e no banco SQLite"

    def handle(self, *args, **options):
        es = Elasticsearch(hosts=["http://localhost:9200"])
        url = "https://www.boticario.com.br/perfumaria/"

        self.stdout.write(self.style.NOTICE(f"Rodando scraper em {url}..."))
        produtos = scrapping(url)

        for produto in produtos:
            # cálculo automático do desconto
            if produto.get("old_price") and produto.get("price"):
                try:
                    desconto = round((1 - produto["price"] / produto["old_price"]) * 100, 2)
                    produto["discount"] = desconto
                except Exception:
                    produto["discount"] = None

            # adicionar timestamp da coleta
            produto["scraped_at"] = datetime.utcnow().isoformat()

            # garantir external_id único
            external_id = gerar_external_id(produto)

            # salvar/atualizar no banco SQLite
            Product.objects.update_or_create(
                external_id=external_id,
                defaults={
                    "source": produto.get("source", "boticario"),
                    "name": produto.get("name"),
                    "brand": produto.get("brand"),
                    "price": produto.get("price"),
                    "old_price": produto.get("old_price"),
                    "discount": produto.get("discount"),
                    "rating": produto.get("rating"),
                    "review_count": produto.get("review_count"),
                    "description": produto.get("description"),
                    "url": produto.get("url"),
                    "image": produto.get("image"),
                    "scraped_at": produto["scraped_at"],
                }
            )

            # salvar/atualizar no Elasticsearch
            es.update(
                index="products",
                id=external_id,
                body={"doc": produto, "doc_as_upsert": True}
            )

        self.stdout.write(
            self.style.SUCCESS(f"{len(produtos)} produtos salvos/atualizados no SQLite e no Elasticsearch.")
        )