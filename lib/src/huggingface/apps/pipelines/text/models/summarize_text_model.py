# generated by datamodel-codegen:
#   filename:  summarize_text_model.json

from __future__ import annotations
from malevich.square import scheme

from typing import Optional

from pydantic import BaseModel, Field


@scheme()
class SummarizeText(BaseModel):
    model: Optional[str] = Field(
        'none', description='Name of the model to use in the pipeline'
    )
