# generated by datamodel-codegen:
#   filename:  send_messages_batch_model.json
#   timestamp: 2024-03-06T12:55:54+00:00

from __future__ import annotations
from malevich.square import scheme

from pydantic import BaseModel, Field


scheme()
class SendMessagesBatch(BaseModel):
    prompt_template: str = Field(
        ...,
        description='A string with the prompt template. The template might contain variables in the following format: {variable_name}. The variables will be replaced with the values from the `input_variables` dataframe for each row',
    )