# generated by datamodel-codegen:
#   filename:  continue_conversation_model.json
#   timestamp: 2024-03-23T14:20:37+00:00

from __future__ import annotations

from typing import Optional

from malevich.square import scheme
from pydantic import BaseModel, Field


@scheme()
class ContinueConversation(BaseModel):
    model: Optional[str] = Field(
        'facebook/blenderbot-400M-distill',
        description='Name of the model to use in the pipeline',
    )
    min_length_for_response: Optional[int] = Field(
        32, description='The minimum length (in number of tokens) for a response'
    )
    minimum_tokens: Optional[int] = Field(
        10, description='The minimum length of tokens to leave for a response'
    )
