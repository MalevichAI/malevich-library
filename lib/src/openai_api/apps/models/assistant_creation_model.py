from __future__ import annotations
from malevich.square import scheme

from typing import List, Optional

from pydantic import BaseModel, Field


@scheme()
class AssistantCreation(BaseModel):
    openai_api_key: str = Field(..., description='Your OpenAI API key')
    model: Optional[str] = Field('gpt-3.5-turbo', description='The model to use')
    organization: Optional[str] = Field(None, description='The organization to use')
    max_retries: Optional[int] = Field(3, description='The maximum number of retries')
    temperature: Optional[float] = Field(0.9, description='The temperature')
    top_p: Optional[float] = Field(1.0, description='The top p')
    response_format: Optional[str] = Field(None, description='The response format')
    