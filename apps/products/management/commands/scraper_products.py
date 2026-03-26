from django.core.management.base import BaseCommand
from apps.products.scraper import scrapping
from elasticsearch import Elasticsearch
from datetime import datetime


from django.core.management.base import BaseCommand
from elasticsearch import Elasticsearch
from apps.products.scraper import scrapping
from datetime import datetime

class Command(BaseCommand):
    help = "Roda o scraper e salva/atualiza os produtos no Elasticsearch"

    def handle(self, *args, **options):
        es = Elasticsearch(hosts=["http://localhost:9200"])
        url = "https://www.boticario.com.br/perfumaria/"

        self.stdout.write(self.style.NOTICE(f"Rodando scraper em {url}..."))
        produtos = scrapping(url)

        for produto in produtos:
            # cálculo automático do desconto
            if produto.get("old_price") and produto.get("price"):
                try:
                    desconto = round(
                        (1 - produto["price"] / produto["old_price"]) * 100, 2
                    )
                    produto["discount"] = desconto
                except Exception:
                    produto["discount"] = None

            # adicionar timestamp da coleta
            produto["scraped_at"] = datetime.utcnow().isoformat()

            # upsert no Elasticsearch
            es.update(
                index="products",
                id=produto["external_id"],
                body={"doc": produto, "doc_as_upsert": True}
            )

        self.stdout.write(
            self.style.SUCCESS(f"{len(produtos)} produtos salvos/atualizados no Elasticsearch.")
        )