class QueryFilterService:
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
        "desodorante": ("category", "desodorante"),
    }

    def extract_filters(self, query: str) -> list[tuple[str, str]]:
        tokens = query.lower().split()
        filters = []

        for token in tokens:
            if token in self.FILTER_MAP:
                filters.append(self.FILTER_MAP[token])

        return filters