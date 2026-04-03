from django_elasticsearch_dsl import Document, Index, fields

from .models import Product


products_index = Index("products")

products_index.settings(
    number_of_shards=1,
    number_of_replicas=0,
)


@products_index.document
class ProductDocument(Document):
    name = fields.TextField(
        attr="name",
        fields={
            "raw": fields.KeywordField(),
        },
    )

    brand = fields.TextField(
        attr="brand",
        fields={
            "raw": fields.KeywordField(),
        },
    )

    description = fields.TextField(attr="description")
    flavor = fields.TextField(attr="flavor")
    target = fields.KeywordField(attr="target")
    category = fields.KeywordField(attr="category")
    source = fields.KeywordField(attr="source")
    external_id = fields.KeywordField(attr="external_id")

    price = fields.FloatField(attr="price")
    old_price = fields.FloatField(attr="old_price")
    discount = fields.IntegerField(attr="discount")

    rating = fields.FloatField(attr="rating")
    review_count = fields.IntegerField(attr="review_count")

    url = fields.KeywordField(attr="url")
    image = fields.KeywordField(attr="image")

    is_active = fields.BooleanField(attr="is_active")
    scraped_at = fields.DateField(attr="scraped_at")
    created_at = fields.DateField(attr="created_at")

    class Django:
        model = Product
        fields = ["id"]