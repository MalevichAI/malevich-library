from typing import Any

from malevich.square import scheme
from pydantic import BaseModel


@scheme()
class Placeholder(BaseModel):
    tokens: dict[int, dict[str, list[Any]]]
