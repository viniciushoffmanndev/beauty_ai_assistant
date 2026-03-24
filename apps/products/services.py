from elasticsearch_dsl import Search, Q
from .es_client import es

def search_products_in_es(query, size=5):
    tokens = query.lower().split()

    q = Q("multi_match", query=query,
          fields=["name^3", "description", "brand", "flavor", "target"],
          fuzziness="AUTO")

    s = Search(using=es, index="products").query(q).filter("term", is_active=True)

    # filtros automáticos
    if "feminino" in tokens:
        s = s.filter("term", target="feminino")
    elif "masculino" in tokens:
        s = s.filter("term", target="masculino")

    if "cítrico" in tokens:
        s = s.filter("term", flavor="cítrico")
    elif "amadeirado" in tokens:
        s = s.filter("term", flavor="amadeirado")

    s = s[:size]
    response = s.execute()

    results = [hit.to_dict() for hit in response]
    return results