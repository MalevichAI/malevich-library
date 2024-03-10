# generated by datamodel-codegen:
#   filename:  combine_vertical_model.json
#   timestamp: 2024-03-06T15:14:51+00:00

from __future__ import annotations
from malevich.square import scheme

from pydantic import BaseModel, Field


scheme()
class CombineVertical(BaseModel):
    ignore_col_names: bool = Field(
        ...,
        description='determines whether to ignore current column names, defaults to False',
    )
    default_name: str = Field(
        ..., description="name template for generic columns names, defaults to 'col'"
    )
    ignore_index: bool = Field(
        ...,
        description='determines whether to ignore dataframe indexes during concatenation, defaults to False',
    )