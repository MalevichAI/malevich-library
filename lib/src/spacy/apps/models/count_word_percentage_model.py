# generated by datamodel-codegen:
#   filename:  count_word_percentage_model.json

from __future__ import annotations

from typing import Optional

from malevich.square import scheme
from pydantic import BaseModel, Field


@scheme()
class CountWordPercentage(BaseModel):
    language: Optional[str] = Field('en', description='Text language')
    delimeter: Optional[str] = Field(',', description='Keywords separator')
    metric_unit: Optional[str] = Field(
        'float', description='Output metric unit. Either "percent" or "float"'
    )
