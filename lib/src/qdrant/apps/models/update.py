from __future__ import annotations
from malevich.square import scheme

from typing import List, Optional

from pydantic import BaseModel, Field
from .qdrant import Qdrant

@scheme()
class Update(Qdrant):
    collection_name: str = Field(..., description='Collection name')
    batch_size: Optional[int] = Field(64, description='Batch size')
    parallel: Optional[int] = Field(1, description='Number of parallel workers')
