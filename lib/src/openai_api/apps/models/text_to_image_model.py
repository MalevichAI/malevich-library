# generated by datamodel-codegen:
#   filename:  text_to_image_model.json
#   timestamp: 2024-03-06T12:55:54+00:00

from __future__ import annotations
from malevich.square import scheme

from typing import Optional

from pydantic import BaseModel, Field


scheme()
class TextToImage(BaseModel):
    openai_api_key: str = Field(..., description='Your OpenAI API key')
    user_prompt: str = Field(..., description='The prompt for the user')
    model: Optional[str] = Field('dall-e-3', description='The model to use')
    download: Optional[bool] = Field(False, description='Whether to download images')
    n: Optional[int] = Field(
        1, description='Amount of images to generate for each request'
    )