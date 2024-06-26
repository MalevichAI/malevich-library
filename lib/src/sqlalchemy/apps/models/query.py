from typing import Optional

from pydantic import Field

from .connection import Connection


class Query(Connection):
    subsequent: Optional[bool] = Field(False, description='Whether each command should be committed or all at once') # noqa:E501
