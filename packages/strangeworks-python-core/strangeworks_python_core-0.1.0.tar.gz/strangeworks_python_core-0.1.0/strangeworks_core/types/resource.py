"""resources.py."""
from dataclasses import dataclass
from typing import Any, Dict, Optional

from strangeworks_core.types.product import Product


@dataclass
class Resource:
    """Represents a Platform Resource object."""

    slug: str
    resource_id: Optional[str] = None
    product: Optional[Product] = None
    name: Optional[str] = None
    status: Optional[str] = None
    is_deleted: Optional[bool] = None

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Resource":
        """Generate a Resource object from a dictionary.

        Parameters
        ----------
        cls
            Class object.
        d: Dict
            Resource object attributes represented as a dictionary.

        Return
        ------
        An intance of the Resource object.
        """
        return cls(
            slug=d.get("slug"),
            resource_id=d.get("id"),
            status=d.get("status"),
            name=d.get("name"),
            product=Product.from_dict(d.get("product")),
            is_deleted=d.get("isDeleted"),
        )

    def proxy_url(self) -> str:
        """Return the proxy URL for the resource.

        Parameters
        ----------
        None

        Returns
        ------
        str:
           url that the proxy will use to make calls to the resource.
        """
        return f"/products/{self.product.slug}/resource/{self.slug}/"
