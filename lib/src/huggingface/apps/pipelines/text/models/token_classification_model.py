# generated by datamodel-codegen:
#   filename:  token_classification_model.json

from __future__ import annotations

from typing import List, Optional

from malevich.square import scheme

from typing import List, Optional

from pydantic import BaseModel, Field


@scheme()
class TokenClassification(BaseModel):
    ignore_labels: Optional[List] = Field(
        ['0'], description='List of labels to ignore (e.g. `["O"]`)'
    )
    keep_text: Optional[bool] = Field(
        False, description="Whether to keep the input text in the output dataframe"
    )
    keep_sentence_index: Optional[bool] = Field(
        True, description="Whether to keep the sentence index in the output dataframe"
    )
    model: Optional[str] = Field(
        None,
        description="Model name (e.g. `dbmdz/bert-large-cased-finetuned-conll03-english`)",
    )
    tokenizer: Optional[str] = Field(
        None, description="Tokenizer name (e.g. `bert-base-cased`)"
    )
    device: Optional[str] = Field(
        "cpu", description="Device to run the model on (`cpu` or `gpu`)"
    )
    batch_size: Optional[int] = Field(1, description="Batch size to use for inference")
    aggregation_strategy: Optional[str] = Field(
        "none",
        description="Aggregation strategy to use for multiple entities per token",
    )
