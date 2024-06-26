from __future__ import annotations

from typing import Optional

from malevich.square import scheme
from pydantic import Field

from .qdrant import Qdrant


@scheme()
class Update(Qdrant):
    collection_name: str = Field(..., description='Collection name')
    batch_size: Optional[int] = Field(64, description='Batch size')  # noqa: E501,UP007
    parallel: Optional[int] = Field(1, description='Number of parallel workers')  # noqa: E501,UP007
