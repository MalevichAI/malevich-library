# generated by datamodel-codegen:
#   filename:  unwrap_model.json
#   timestamp: 2024-03-13T13:09:13+00:00

from __future__ import annotations

from typing import Optional

from malevich.square import scheme
from pydantic import BaseModel, Field

scheme()
class Unwrap(BaseModel):
    columns: Optional[list[str]] = Field(
        ['all'],
        description='The columns to unwrap. If not specified, all columns will be unwrapped',
    )
    delimiter: Optional[str] = Field(
        ',',
        description='The delimiter used to separate values in the columns. If not specified, the default delimiter is a comma (,)',
    )
