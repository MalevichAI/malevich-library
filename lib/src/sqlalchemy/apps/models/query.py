from typing import Optional

from malevich.square import scheme
from pydantic import Field

from .connection import Connection


@scheme()
class Query(Connection):
    subsequent: Optional[bool] = Field(False, description='Whether each command should be committed or all at once') # noqa:E501
    format: Optional[dict[str, str]] = Field(None, description='Values of tokens that are being substituted') # noqa:E501
