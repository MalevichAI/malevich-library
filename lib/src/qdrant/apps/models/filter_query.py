from __future__ import annotations

from typing import Optional

from malevich.square import scheme
from pydantic import Field

from .filter import Filter
from .query import Query


@scheme()
class FilterQuery(Query):
    filter: Optional[Filter] = Field(None, description="Qdrant filter")
    limit: Optional[int] = Field(10, description="How many points should the query return") # noqa:E501
