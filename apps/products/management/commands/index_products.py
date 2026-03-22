from django.core.management.base import BaseCommand
from elasticsearch import Elasticsearch
from apps.products.models import Product

es = Elasticsearch("http://localhost:9200",
                   basic_auth=("elastic", "130622"))  # Ajuste as credenciais conforme necessário

class Command(BaseCommand):
    help = "Indexa produtos no Elasticsearch"

    def handle(self, *args, **kwargs):
        for product in Product.objects.filter(is_active=True):
            doc = {
                "name": product.name,
                "brand": product.brand,
                "flavor": product.flavor,
                "target": product.target,
                "description": product.description,
                "price": float(product.price),
                "is_active": product.is_active,
            }
            es.index(index="products", id=product.id, document=doc)
        self.stdout.write(self.style.SUCCESS("Produtos indexados com sucesso!"))