# generated by datamodel-codegen:
#   filename:  locs_model.json

from __future__ import annotations

from typing import List, Optional

from malevich.square import scheme

from typing import List, Optional

from pydantic import BaseModel, Field


@scheme()
class Locs(BaseModel):
    column: Optional[str] = Field(None, description='The column to be extracted')
    columns: Optional[List[str]] = Field(
        None, description='The columns to be extracted'
    )
    columns_expr: Optional[List[str]] = Field(
        None,
        description='The list of expressions to retrieve columns. Each expression is in form `start:(end):(skip)`. Examples: 0:, :10, 0:10, 0::2, 0:10:2.',
    )
    column_idx: Optional[int] = Field(
        None, description='The column index to be extracted'
    )
    column_idxs: Optional[List[int]] = Field(
        None, description='The column indexes to be extracted'
    )
    row: Optional[int] = Field(None, description='The row to be extracted')
    rows: Optional[List[int]] = Field(None, description='The rows to be extracted')
    row_idx: Optional[int] = Field(None, description='The row index to be extracted')
    row_idxs: Optional[List[int]] = Field(
        None, description='The row indexes to be extracted'
    )
    rows_expr: Optional[List[str]] = Field(
        None,
        description='The list of expressions to retrieve rows. Each expression is in form `start:(end):(skip)`. Examples: 0:, :10, 0:10, 0::2, 0:10:2.',
    )
    unique: Optional[bool] = Field(
        False,
        description='Get unique values from column. Must be used with `column` or `column_idx`',
    )
