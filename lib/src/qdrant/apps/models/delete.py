from __future__ import annotations

from malevich.square import scheme
from pydantic import Field

from .qdrant import Qdrant


@scheme()
class Delete(Qdrant):
    collection_name: str = Field(..., description='Collection name')
    ordering: str | None = Field(None, description='Ordering')