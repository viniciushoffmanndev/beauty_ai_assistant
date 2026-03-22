from django.conf import settings
from elasticsearch import Elasticsearch

es = Elasticsearch(
    settings.ELASTICSEARCH_URL,
    basic_auth=(settings.ELASTICSEARCH_USER, settings.ELASTICSEARCH_PASSWORD)
)