from __future__ import annotations

from typing import Optional

from malevich.square import scheme
from pydantic import BaseModel, Field


@scheme()
class MinShould(BaseModel, extra="forbid"):
    conditions: list = Field(..., description="")
    min_count: int = Field(..., description="")

@scheme()
class Filter(BaseModel, extra="forbid"):
    should: Optional[list] = Field(
        default=None, description="At least one of those conditions should match"
    )
    min_should: Optional["MinShould"] = Field(
        default=None, description="At least minimum amount of given conditions should match" # noqa:E501
    )
    must: Optional[list] = Field(default=None, description="All conditions must match")
    must_not: Optional[list] = Field(default=None, description="All conditions must NOT match") # noqa:E501
