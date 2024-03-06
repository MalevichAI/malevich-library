# generated by datamodel-codegen:
#   filename:  rename_model.json
#   timestamp: 2024-03-06T12:29:19+00:00

from __future__ import annotations
from malevich.square import scheme

from typing import Optional

from pydantic import BaseModel, Field


scheme()
class Rename(BaseModel):
    old_column_name: Optional[str] = Field(
        "''",
        description="Provides mapping of old column names to their new names. For example 'a': 'A'",
    )
