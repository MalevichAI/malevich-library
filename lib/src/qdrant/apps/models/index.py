from __future__ import annotations

from enum import Enum
from typing import Optional

from malevich.square import scheme
from pydantic import BaseModel, Field

# from qdrant_client.models import IntegerIndexParams, SparseIndexParams, TextIndexParams
from .qdrant import Qdrant


class IntegerIndexParams(BaseModel, extra="forbid"):
    type: str = Field(..., description="")
    lookup: bool = Field(..., description="If true - support direct lookups.")
    range: bool = Field(..., description="If true - support ranges filters.")


class SparseIndexParams(BaseModel, extra="forbid"):
    """
    Configuration for sparse inverted index.
    """

    full_scan_threshold: Optional[int] = Field(
        default=None,
        description="We prefer a full scan search upto (excluding) this number of vectors.  Note: this is number of vectors, not KiloBytes.",
    )
    on_disk: Optional[bool] = Field(
        default=None,
        description="Store index on disk. If set to false, the index will be stored in RAM. Default: false",
    )

class TextIndexParams(BaseModel, extra="forbid"):
    type: str = Field(..., description="")
    tokenizer: Optional[str] = Field(default=None, description="")
    min_token_len: Optional[int] = Field(default=None, description="")
    max_token_len: Optional[int] = Field(default=None, description="")
    lowercase: Optional[bool] = Field(default=None, description="If true, lowercase all tokens. Default: true")


@scheme()
class Index(Qdrant):
    schema: TextIndexParams | SparseIndexParams | IntegerIndexParams = Field(
        ...,
        description='Native Qdrant index parameters'
    )
