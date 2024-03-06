# generated by datamodel-codegen:
#   filename:  generate_audio_model.json
#   timestamp: 2024-03-06T12:29:20+00:00

from __future__ import annotations
from malevich.square import scheme

from pydantic import BaseModel, Field


scheme()
class GenerateAudio(BaseModel):
    replicate_api_key: str = Field(
        ..., description='[Replicate](https://replicate.com/) API key'
    )
    save_prefix: str = Field(..., description='Prefix path to save the audio in')
