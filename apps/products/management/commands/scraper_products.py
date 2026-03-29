import hashlib
import logging

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.products.models import Product
from apps.products.scraper.boticario import BoticarioScraper

logger = logging.getLogger(__name__)


def gerar_external_id(produto: dict) -> str:
    """
    Gera um external_id único.
    Se já existir no produto, usa ele.
    Caso contrário, gera um hash da URL.
    """
    if produto.get("external_id"):
        return produto["external_id"]

    url = produto.get("url", "")
    return hashlib.md5(url.encode()).hexdigest()


class Command(BaseCommand):
    help = "Executa o scraper e salva/atualiza os produtos no banco"

    def handle(self, *args, **options):
        url = "https://www.boticario.com.br/lancamentos/"

        self.stdout.write("Iniciando scraping de produtos...")

        scraper = BoticarioScraper()
        products_data = scraper.scrape(url)

        created_count = 0
        updated_count = 0
        ignored_count = 0

        with transaction.atomic():
            for data in products_data:
                try:
                    external_id = gerar_external_id(data)

                    if not external_id or not data.get("name"):
                        ignored_count += 1
                        logger.warning(
                            "Produto ignorado por falta de external_id ou name | data=%s",
                            data,
                        )
                        continue

                    obj, created = Product.objects.update_or_create(
                        external_id=external_id,
                        source=data.get("source", "boticario"),
                        defaults={
                            "name": data.get("name"),
                            "brand": data.get("brand"),
                            "price": data.get("price"),
                            "old_price": data.get("old_price"),
                            "discount": data.get("discount"),
                            "rating": data.get("rating"),
                            "review_count": data.get("review_count"),
                            "description": data.get("description"),
                            "url": data.get("url"),
                            "image": data.get("image"),
                        },
                    )

                    if created:
                        created_count += 1
                    else:
                        updated_count += 1

                except Exception as exc:
                    ignored_count += 1
                    logger.exception("Erro ao salvar produto no banco: %s", exc)

        self.stdout.write(
            self.style.SUCCESS(
                "Scraping concluído com sucesso | "
                f"criados={created_count} | "
                f"atualizados={updated_count} | "
                f"ignorados={ignored_count}"
            )
        )