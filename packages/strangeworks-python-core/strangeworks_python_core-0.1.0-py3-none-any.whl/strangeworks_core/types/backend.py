"""backends.py."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from strangeworks_core.types.product import Product
from strangeworks_core.utils import is_empty_str, str_to_datetime


class Status(Enum):
    """Enumeration of possible backend statuses."""

    ONLINE = "online"
    OFFILE = "offline"
    MAINTENANCE = "maintenance"
    RETIRED = "retired"
    UNKNOWN = "unknown"

    @staticmethod
    def from_str(s: Optional[str] = None):
        """Return Status from string."""
        if is_empty_str(s):
            return Status.UNKNOWN
        adj_str = s.strip().lower()
        possible_ans = [e for e in Status if e.value == adj_str]
        if len(possible_ans) != 1:
            return Status.UNKNOWN
        return possible_ans[0]


@dataclass
class Backend:
    """Represents a Strangeworks platform Backend object."""

    name: str
    slug: str
    status: str
    product: Optional[Product] = None
    backend_id: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    data_schema: Optional[str] = None
    remote_backend_id: Optional[str] = None
    remote_status: Optional[str] = None
    date_created: Optional[datetime] = None
    date_updated: Optional[datetime] = None

    @classmethod
    def from_dict(cls, backend: dict) -> Backend:
        return cls(
            name=backend.get("name"),
            slug=backend.get("slug"),
            status=Status.from_str(backend.get("status")),
            date_created=str_to_datetime(backend.get("dateCreated")),
            date_updated=str_to_datetime(backend.get("dateUpdated")),
            product=Product.from_dict(backend.get("product")),
            backend_id=backend.get("id"),
            data=backend.get("data"),
            data_schema=backend.get("data_schema"),
            remote_backend_id=backend.get("remoteBackendId"),
            remote_status=backend.get("remoteStatus"),
        )
