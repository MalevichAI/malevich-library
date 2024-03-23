# generated by datamodel-codegen:
#   filename:  squash_columns_model.json
#   timestamp: 2024-03-23T14:20:36+00:00

from __future__ import annotations

from typing import Optional

from malevich.square import scheme
from pydantic import BaseModel, Field


@scheme()
class SquashColumns(BaseModel):
    columns: Optional[list[str]] = Field(
        None,
        description='The columns to squash. If not specified, all columns will be squashed',
    )
    result_column_name: Optional[str] = Field(
        None,
        description='The name of the resulting column. If not specified, the default name is the concatenation of the column names',
    )
    drop: Optional[bool] = Field(
        False,
        description='Whether to drop the original columns. If not specified, the default value is False',
    )
    delim: Optional[str] = Field(
        ',',
        description='The delimiter used to separate values in the columns. If not specified, the default delimiter is a comma (,)',
    )
