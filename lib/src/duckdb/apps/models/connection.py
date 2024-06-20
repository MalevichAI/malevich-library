from pydantic import BaseModel, Field
from malevich.square import scheme
from typing import Optional

@scheme()
class Connection(BaseModel):
    db_name: str = Field(..., description="Name of the database to connect to")
    read_only: Optional[bool] = Field(True, description="Access levels of the connection")