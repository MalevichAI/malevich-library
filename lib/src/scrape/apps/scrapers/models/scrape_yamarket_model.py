# generated by datamodel-codegen:
#   filename:  scrape_yamarket_model.json

from __future__ import annotations
from malevich.square import scheme

from typing import Optional

from pydantic import BaseModel, Field


@scheme()
class ScrapeYamarket(BaseModel):
    max_results: Optional[int] = Field(
        3, description='The amount of images to retrieve'
    )
