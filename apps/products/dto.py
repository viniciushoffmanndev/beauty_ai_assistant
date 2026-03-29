from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass
class ProductScrapedDTO:
    external_id: str
    source: str
    name: str
    brand: Optional[str]
    price: Optional[Decimal]
    old_price: Optional[Decimal]
    discount: Optional[int]
    rating: Optional[float]
    review_count: Optional[int]
    description: Optional[str]
    url: Optional[str]
    image: Optional[str]

    def to_dict(self) -> dict:
        return {
            "external_id": self.external_id,
            "source": self.source,
            "name": self.name,
            "brand": self.brand,
            "price": float(self.price) if self.price is not None else None,
            "old_price": float(self.old_price) if self.old_price is not None else None,
            "discount": self.discount,
            "rating": self.rating,
            "review_count": self.review_count,
            "description": self.description,
            "url": self.url,
            "image": self.image,
        }
    