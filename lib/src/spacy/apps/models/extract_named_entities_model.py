# generated by datamodel-codegen:
#   filename:  extract_named_entities_model.json
#   timestamp: 2024-03-06T12:55:54+00:00

from __future__ import annotations
from malevich.square import scheme

from typing import List, Optional

from pydantic import BaseModel, Field


scheme()
class ExtractNamedEntities(BaseModel):
    output_format: Optional[str] = Field(
        'list',
        description='The format of the output. Valid values are "list", "struct", and "table"',
    )
    model_name: Optional[str] = Field(
        'en_core_web_sm',
        description='The name of the model to use. See https://spacy.io/models for available models',
    )
    filter_labels: Optional[List[str]] = Field(
        None,
        description='A list of labels to filter the named entities by. If None, all named entities will be returned',
    )