# generated by datamodel-codegen:
#   filename:  squash_model.json
#   timestamp: 2024-03-23T14:20:36+00:00

from __future__ import annotations

from typing import Optional

from malevich.square import scheme
from pydantic import BaseModel, Field


@scheme()
class Squash(BaseModel):
    by: Optional[str] = Field(
        'all',
        description='The column to group by. If not specified, all columns will be squashed',
    )
    delim: Optional[str] = Field(
        ',',
        description='The delimiter used to separate values in the columns. If not specified, the default delimiter is a comma (,)',
    )
