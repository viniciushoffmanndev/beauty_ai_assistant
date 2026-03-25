from elasticsearch_dsl import Search, Q
from .es_client import es

# Mapeamento de tokens → campos do ES
FILTER_MAP = {
    "feminino": ("target", "feminino"),
    "masculino": ("target", "masculino"),
    "unissex": ("target", "unissex"),
    "cítrico": ("flavor", "cítrico"),
    "amadeirado": ("flavor", "amadeirado"),
    "floral": ("flavor", "floral"),
    "doce": ("flavor", "doce"),
    "oriental": ("flavor", "oriental"),
    "frutal": ("flavor", "frutal"),
    "colônia": ("category", "colônia"),
    "perfume": ("category", "perfume"),
    "body": ("category", "body splash"),
    "desodorante": ("category", "desodorante")
}

def search_products_in_es(query, size=5):
    tokens = query.lower().split()

    # busca principal com relevância
    q = Q("multi_match", query=query,
          fields=["name^3", "description", "brand", "flavor", "target", "category"],
          fuzziness="AUTO")

    s = Search(using=es, index="products").query(q).filter("term", is_active=True)

    # aplica filtros automáticos baseados em tokens
    for token in tokens:
        if token in FILTER_MAP:
            field, value = FILTER_MAP[token]
            s = s.filter("term", **{field: value})

    s = s[:size]
    response = s.execute()

    results = [hit.to_dict() for hit in response]
    return results