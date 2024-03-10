# generated by datamodel-codegen:
#   filename:  subset_model.json
#   timestamp: 2024-03-06T17:15:23+00:00

from __future__ import annotations
from malevich.square import scheme

from pydantic import BaseModel, Field


scheme()
class Subset(BaseModel):
    expr: str = Field(
        ...,
        description='A comma-separated list of integers or slices, e.g. `0,1:3,5:7,6,9:10`. The first dataframe has index 0',
    )