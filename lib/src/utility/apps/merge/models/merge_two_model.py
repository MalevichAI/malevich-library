# generated by datamodel-codegen:
#   filename:  merge_two_model.json
#   timestamp: 2024-03-06T15:14:51+00:00

from __future__ import annotations
from malevich.square import scheme

from typing import List, Optional, Union

from pydantic import BaseModel, Field


scheme()
class MergeTwo(BaseModel):
    how: Optional[str] = Field('inner', description='The type of merge to be performed')
    both_on: Optional[Union[str, List]] = Field(
        '',
        description="Column name or 'index' to merge on. If 'index', the index of the dataframe will be used. If column name, the column should be present in all dataframes",
    )
    left_on: Optional[Union[str, List]] = Field(
        '',
        description="Column name or 'index' to join on in the left DataFrame. If 'index', the index of the dataframe will be used. If column name, the column should be present in all but last dataframes",
    )
    right_on: Optional[Union[str, List]] = Field(
        '',
        description="Column name or 'index' to join on in the right DataFrame. If 'index', the index of the dataframe will be used. If column name, the column should be present in all but first dataframes",
    )
    suffixes: Optional[List] = Field(
        ['_0', '_1'],
        description='Suffix to apply to overlapping column names in the left and right dataframes',
    )
