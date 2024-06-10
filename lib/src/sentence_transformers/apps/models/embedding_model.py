from __future__ import annotations

from typing import Optional

from malevich.square import scheme
from pydantic import BaseModel, Field


@scheme()
class Embedding(BaseModel):
    model: Optional[str] = Field('all-MiniLM-L6-v2', description='The model to use')
    device: Optional[str] = Field('cpu', description='The device to run on')
    mode: Optional[str] = Field('sentence_embedding', description='Output mode')
    batch_size: Optional[int] = Field(32,  description='Batch size')
