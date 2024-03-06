# generated by datamodel-codegen:
#   filename:  assert_links_model.json
#   timestamp: 2024-03-06T12:29:20+00:00

from __future__ import annotations
from malevich.square import scheme

from typing import Optional

from pydantic import BaseModel, Field


scheme()
class AssertLinks(BaseModel):
    filter_links: Optional[bool] = Field(
        False,
        description='If set to True, will filter the dataframe and exclude invalid links',
    )
