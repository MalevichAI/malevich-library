from malevich.square import scheme
from pydantic import Field


@scheme()
class Connection:
    url: str = Field(..., description='URL for DB connection')
