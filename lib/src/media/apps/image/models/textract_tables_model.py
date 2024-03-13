# generated by datamodel-codegen:
#   filename:  textract_tables_model.json
#   timestamp: 2024-03-13T12:49:28+00:00

from __future__ import annotations

from typing import Optional

from malevich.square import scheme
from pydantic import BaseModel, Field

scheme()
class TextractTables(BaseModel):
    aws_access_key_id: str = Field(..., description='Your AWS access key ID')
    aws_secret_access_key: str = Field(..., description='Your AWS secret access key')
    write_contents: Optional[bool] = Field(
        False, description='Whether to write the contents of the table to the output'
    )
