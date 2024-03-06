# generated by datamodel-codegen:
#   filename:  download_model.json
#   timestamp: 2024-03-06T12:29:19+00:00

from __future__ import annotations
from malevich.square import scheme

from typing import Optional

from pydantic import BaseModel, Field


scheme()
class Download(BaseModel):
    prefix: Optional[str] = Field(
        '',
        description='A prefix to add to the paths of downloaded files. If not specified, files will be downloaded to the root of the app directory',
    )
