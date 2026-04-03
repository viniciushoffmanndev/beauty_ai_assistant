from django.conf import settings
from elasticsearch import Elasticsearch


es = Elasticsearch(
    hosts=[settings.ELASTICSEARCH_DSL["default"]["hosts"]],
    verify_certs=False,
)