from __future__ import annotations
from malevich.square import scheme

from typing import List, Optional

from pydantic import BaseModel, Field


@scheme()
class ThreadPromptCompletion(BaseModel):
    openai_api_key: str = Field(..., description='Your OpenAI API key')
    assistant_id: str = Field(..., description='The id of the assistant')
    model: Optional[str] = Field('gpt-3.5-turbo', description='The model to use')
    organization: Optional[str] = Field(None, description='The organization to use')
    max_retries: Optional[int] = Field(3, description='The maximum number of retries')
    temperature: Optional[float] = Field(0.9, description='The temperature')
    max_tokens: Optional[int] = Field(150, description='The maximum number of tokens')
    top_p: Optional[float] = Field(1.0, description='The top p')
    frequency_penalty: Optional[float] = Field(0.0, description='The frequency penalty')
    presence_penalty: Optional[float] = Field(0.0, description='The presence penalty')
    stop: Optional[List] = Field([], description='The stop tokens')
    stream: Optional[bool] = Field(False, description='Whether to stream the response')
    n: Optional[int] = Field(1, description='The number of completions to generate')
    response_format: Optional[str] = Field(None, description='The response format')
