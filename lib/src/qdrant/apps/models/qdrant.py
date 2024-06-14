from __future__ import annotations
from malevich.square import scheme

from typing import List, Optional

from pydantic import BaseModel, Field


@scheme()
class Qdrant(BaseModel):
    url: str = Field(..., description='Your Qdrant url')
    api_key: str | None = Field(None, description='Your Qdrant API key')
    timeout: int | None = Field(None, description='REST timeout')
    https: bool | None = Field(None, description='Is HTTPS being used?')
