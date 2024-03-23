# generated by datamodel-codegen:
#   filename:  continue_conversation_model.json

from __future__ import annotations
from malevich.square import scheme

from typing import Optional

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
