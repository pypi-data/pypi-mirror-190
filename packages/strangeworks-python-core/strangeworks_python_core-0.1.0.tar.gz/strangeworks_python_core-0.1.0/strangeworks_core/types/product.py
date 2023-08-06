"""product.py."""
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class Product:
    """Represents a Platform Product object."""

    slug: str
    product_id: Optional[str] = None
    name: Optional[str] = None

    @classmethod
    def from_dict(cls, d: Dict[str, str]) -> "Product":
        """Create a Product object from Dictionary."""
        return cls(
            slug=d.get("slug"),
            name=d.get("name"),
            product_id=d.get("id"),
        )
