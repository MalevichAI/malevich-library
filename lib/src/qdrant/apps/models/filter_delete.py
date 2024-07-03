from __future__ import annotations

from malevich.square import scheme
from pydantic import Field

from .delete import Delete
from .filter import Filter


@scheme()
class FilterDelete(Delete):
    filter: Filter = Field(..., description='Conditions for deletion')
