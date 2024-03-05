# generated by datamodel-codegen:
#   filename:  completion_with_vision_model.json
#   timestamp: 2024-03-05T17:40:29+00:00

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class CompletionWithVision(BaseModel):
    openai_api_key: str = Field(..., description='Your OpenAI API key')
    user_prompt: str = Field(..., description='The prompt for the user')
    image_column: Optional[str] = Field('images', description='The column with images')
    max_tokens: Optional[int] = Field(2048, description='The maximum number of tokens')
    top_p: Optional[float] = Field(
        1.0,
        description='The probability of the model returning a next token that is in the top P tokens',
    )
    temperature: Optional[float] = Field(
        1.0, description='The higher the value, the more random the generated text'
    )
    frequency_penalty: Optional[float] = Field(
        0.0,
        description='The higher the value, the less likely the model is to repeat the same word',
    )
    presence_penalty: Optional[float] = Field(
        0.0,
        description='The higher the value, the less likely the model is to talk about the same topic again',
    )
    model: Optional[str] = Field('gpt-4-vision-preview', description='The model to use')
