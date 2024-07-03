# generated by datamodel-codegen:
#   filename:  scrape_aliexpress_model.json

from __future__ import annotations
from malevich.square import scheme

from typing import Optional

from pydantic import BaseModel, Field


@scheme()
class ScrapeAliexpress(BaseModel):
    max_results: Optional[int] = Field(None, description='Max images to retrieve')
    only_images: Optional[bool] = Field(False, description='Get only images DataFrame')
    only_properties: Optional[bool] = Field(
        False, description='Get only properties DataFrame'
    )
    output_type: Optional[str] = Field(
        'text', description="Format of text data. Either 'text' or 'json'"
    )
