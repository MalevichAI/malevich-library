from __future__ import annotations

from typing import Optional

from malevich.square import scheme
from pydantic import Field

from .filter_query import FilterQuery


@scheme()
class SearchQuery(FilterQuery):
    score_threshold: Optional[float] = Field(0.0, description="Score threshold")
