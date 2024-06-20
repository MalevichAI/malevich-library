from .connection import Connection
from pydantic import Field
from malevich.square import scheme
from typing import Optional


@scheme()
class QueryConfig(Connection):
    table_format: dict[str, str] = Field(..., description="Table names for query substitution")

