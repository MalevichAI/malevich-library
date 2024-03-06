# generated by datamodel-codegen:
#   filename:  token_classification_model.json
#   timestamp: 2024-03-06T12:29:20+00:00

from __future__ import annotations
from malevich.square import scheme

from typing import List

from pydantic import BaseModel, Field


scheme()
class TokenClassification(BaseModel):
    ignore_labels: List = Field(
        ..., description='List of labels to ignore (e.g. `["O"]`)'
    )
    keep_text: bool = Field(
        ..., description='Whether to keep the input text in the output dataframe'
    )
    keep_sentence_index: bool = Field(
        ..., description='Whether to keep the sentence index in the output dataframe'
    )
    model: str = Field(
        ...,
        description='Model name (e.g. `dbmdz/bert-large-cased-finetuned-conll03-english`)',
    )
    tokenizer: str = Field(..., description='Tokenizer name (e.g. `bert-base-cased`)')
    device: str = Field(..., description='Device to run the model on (`cpu` or `gpu`)')
    batch_size: int = Field(..., description='Batch size to use for inference')
    aggregation_strategy: str = Field(
        ..., description='Aggregation strategy to use for multiple entities per token'
    )
