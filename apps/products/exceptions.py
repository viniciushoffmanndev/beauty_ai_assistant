class ScraperError(Exception):
    """Erro base do scraper."""


class ScraperRequestError(ScraperError):
    """Erro ao buscar a página."""


class ScraperStructureChangedError(ScraperError):
    """Estrutura HTML mudou ou nenhum produto foi encontrado."""


class ProductParseError(ScraperError):
    """Erro ao fazer parse de um produto."""


class EmbeddedJsonParseError(ProductParseError):
    """Erro ao interpretar JSON embutido no HTML."""