import unicodedata


class QueryFilterService:
    FILTER_MAP = {
        "feminino": ("target", "feminino"),
        "masculino": ("target", "masculino"),
        "unissex": ("target", "unissex"),
        "citrico": ("flavor", "cítrico"),
        "cítrico": ("flavor", "cítrico"),
        "amadeirado": ("flavor", "amadeirado"),
        "floral": ("flavor", "floral"),
        "doce": ("flavor", "doce"),
        "oriental": ("flavor", "oriental"),
        "frutal": ("flavor", "frutal"),
        "colonia": ("category", "colonia"),
        "colônia": ("category", "colonia"),
        "perfume": ("category", "perfume"),
        "body": ("category", "body splash"),
        "splash": ("category", "body splash"),
        "desodorante": ("category", "desodorante"),
    }

    @staticmethod
    def _normalize(text: str) -> str:
        text = unicodedata.normalize("NFKD", text.lower())
        return "".join(ch for ch in text if not unicodedata.combining(ch))

    def extract_filters(self, query: str) -> list[tuple[str, str]]:
        tokens = self._normalize(query).split()
        seen: set[tuple[str, str]] = set()
        filters: list[tuple[str, str]] = []

        for token in tokens:
            item = self.FILTER_MAP.get(token)
            if item and item not in seen:
                seen.add(item)
                filters.append(item)

        return filters

    def clean_query(self, query: str) -> str:
        tokens = self._normalize(query).split()
        clean_tokens = [token for token in tokens if token not in self.FILTER_MAP]
        return " ".join(clean_tokens).strip()
