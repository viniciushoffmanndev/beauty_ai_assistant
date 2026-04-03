import json
import logging
from decimal import Decimal, InvalidOperation
from typing import Optional

import requests
from bs4 import BeautifulSoup, Tag

from apps.products.constants import (
    BOTICARIO_SOURCE,
    DEFAULT_HEADERS,
    MIN_VALID_PRODUCTS,
)
from apps.products.dto import ProductScrapedDTO
from apps.products.exceptions import (
    EmbeddedJsonParseError,
    ProductParseError,
    ScraperRequestError,
    ScraperStructureChangedError,
)
from apps.products.validators import validate_product

logger = logging.getLogger(__name__)


class BoticarioScraper:
    def __init__(self, timeout: int = 10):
        self.timeout = timeout

    def scrape(self, url: str) -> list[dict]:
        html = self._fetch_page(url)
        products = self._parse_products(html)

        if len(products) < MIN_VALID_PRODUCTS:
            raise ScraperStructureChangedError(
                f"Poucos produtos válidos encontrados: {len(products)}"
            )

        logger.info(
            "Scraping concluído com sucesso | produtos_validos=%s",
            len(products),
        )

        return [product.to_dict() for product in products]

    def _fetch_page(self, url: str) -> str:
        try:
            response = requests.get(
                url,
                headers=DEFAULT_HEADERS,
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.text

        except requests.RequestException as exc:
            logger.exception("Erro ao acessar URL do scraper | url=%s", url)
            raise ScraperRequestError(f"Erro ao acessar URL: {url}") from exc

    def _parse_products(self, html: str) -> list[ProductScrapedDTO]:
        soup = BeautifulSoup(html, "html.parser")
        articles = soup.find_all("article")

        if not articles:
            raise ScraperStructureChangedError(
                "Nenhum produto encontrado — possível mudança no site"
            )

        products = []
        errors = 0

        for item in articles:
            try:
                product = self._parse_product(item)
                validate_product(product.to_dict())
                products.append(product)

            except Exception as exc:
                errors += 1
                logger.warning(
                    "Erro ao processar produto individual no scraper: %s",
                    exc,
                    exc_info=True,
                )

        logger.info(
            "Parse finalizado | produtos_validos=%s | erros=%s",
            len(products),
            errors,
        )

        return products

    def _parse_product(self, item: Tag) -> ProductScrapedDTO:
        try:
            name = self._get_text(item, "span", class_="showcase-item-title")
            brand = self._get_text(item, "span", class_="showcase-item-brand")

            price = self._parse_price(
                self._get_text(item, "span", class_="price-value")
            )
            old_price = self._parse_price(
                self._get_text(item, "div", class_="item-price-max")
            )
            discount = self._parse_discount(
                self._get_text(item, "span", class_="item-discount")
            )
            description = self._get_text(
                item, "p", class_="showcase-item-description"
            )

            link = self._get_attr(
                item, "a", "href", class_="showcase-item-name"
            )
            image = self._extract_image(item)

            rating, review_count = self._extract_rating_data(item)
            raw_data = self._parse_embedded_json(item.get("data-event", ""))

            return ProductScrapedDTO(
                external_id=raw_data.get("sku", ""),
                source=BOTICARIO_SOURCE,
                name=name or "",
                brand=brand,
                price=price,
                old_price=old_price,
                discount=discount,
                rating=rating,
                review_count=review_count,
                description=description,
                url=link,
                image=image,
            )

        except Exception as exc:
            raise ProductParseError("Falha ao interpretar produto") from exc

    @staticmethod
    def _get_text(parent: Tag, tag: str, **kwargs) -> Optional[str]:
        element = parent.find(tag, **kwargs)
        return element.get_text(strip=True) if element else None

    @staticmethod
    def _get_attr(parent: Tag, tag: str, attr_name: str, **kwargs) -> Optional[str]:
        element = parent.find(tag, **kwargs)
        return element.get(attr_name) if element else None

    @staticmethod
    def _parse_price(value: Optional[str]) -> Optional[Decimal]:
        if not value:
            return None

        try:
            cleaned = (
                value.replace("R$", "")
                .replace(".", "")
                .replace(",", ".")
                .strip()
            )
            return Decimal(cleaned)

        except (InvalidOperation, AttributeError):
            return None

    @staticmethod
    def _parse_discount(value: Optional[str]) -> Optional[int]:
        if not value:
            return None

        try:
            return int(value.replace("-", "").replace("%", "").strip())
        except ValueError:
            return None

    @staticmethod
    def _extract_image(item: Tag) -> Optional[str]:
        img = item.find("img")
        if not img:
            return None

        return img.get("data-src") or img.get("data-original") or img.get("src")

    @staticmethod
    def _extract_rating_data(item: Tag) -> tuple[Optional[float], Optional[int]]:
        rating_div = item.find("div", class_="showcase-item-rating")

        if not rating_div:
            return None, None

        rating = None
        reviews = None

        aria = rating_div.get("aria-label", "")
        title = rating_div.get("title", "")

        try:
            if "Nota" in aria:
                rating = float(aria.split(" ")[1])
        except (ValueError, IndexError):
            rating = None

        try:
            if "avaliações" in title:
                reviews = int(title.split(" ")[0])
        except (ValueError, IndexError):
            reviews = None

        return rating, reviews

    @staticmethod
    def _parse_embedded_json(raw_value: str) -> dict:
        if not raw_value:
            return {}

        try:
            normalized = raw_value.replace("&quot;", '"')
            return json.loads(normalized)
        except json.JSONDecodeError as exc:
            logger.warning(
                "Erro ao interpretar data-event do scraper | raw_value=%s",
                raw_value[:300],
            )
            raise EmbeddedJsonParseError("Erro ao interpretar data-event") from exc
