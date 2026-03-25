from django_elasticsearch_dsl import Document, Index, fields
from .models import Product

products_index = Index("products")

@products_index.document
class ProductDocument(Document):
    class Django:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "brand",
            "price",
            "discount",
            "rating",
            "review_count",
            "is_active",
            "scraped_at",
        ]