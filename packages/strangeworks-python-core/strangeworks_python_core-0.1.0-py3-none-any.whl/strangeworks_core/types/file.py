"""file.py."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class File:
    """Class that represents a file associated with a job."""

    slug: str = None
    file_id: Optional[str] = None
    label: Optional[str] = None
    file_name: Optional[str] = None
    url: Optional[str] = None

    @classmethod
    def from_dict(cls, d: dict) -> "File":
        return cls(
            file_id=d.get("id"),
            slug=d.get("slug"),
            label=d.get("label"),
            url=d.get("url"),
            file_name=d.get("fileName"),
        )
