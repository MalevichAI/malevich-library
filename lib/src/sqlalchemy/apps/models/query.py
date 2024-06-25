from typing import Optional

from pydantic import Field

from .connection import Connection


class Query(Connection):
    subsequent: Optional[bool] = Field(True, description='Submit subsequently')
