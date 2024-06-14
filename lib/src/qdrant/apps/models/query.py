from __future__ import annotations

from malevich.square import scheme
from pydantic import BaseModel, Field
from typing import Optional, Union
from .qdrant import Qdrant

@scheme()
class Query(Qdrant):
    collection_name: str = Field(..., description='Collection name')
    with_vectors: list[str] | bool = Field(True, description='Vectors to choose')
    with_payload: list[str] | bool = Field(True, description='Payload to choose')
