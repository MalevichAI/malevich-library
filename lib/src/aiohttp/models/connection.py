from malevich.square import scheme

from pydantic import BaseModel, Field
from typing import Optional

@scheme()
class Connection(BaseModel):
    base_url: str = Field(..., description="Base URL to connect to")
    timeout: Optional[float] = Field(None, description="Timeout in seconds")
    interval: Optional[float] = Field(None, description="Intervals between operations in seconds")