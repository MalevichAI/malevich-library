from __future__ import annotations

from typing import Optional

from malevich.square import scheme
from pydantic import Field
from qdrant_client.models import (
    HnswConfig,
    OptimizersConfig,
    QuantizationConfig,
    VectorsConfig,
    WalConfig,
)

from .qdrant import Qdrant


@scheme()
class Create(Qdrant):
    vectors: VectorsConfig = Field(..., description="Vector configuration")
    hnsw_config: Optional[HnswConfig] = Field(None, description="HNSW config")
    wal_config: Optional[WalConfig] = Field(None, description="WAL config")
    optimizers_config: Optional[OptimizersConfig] = Field(None, description="Optimizers config") # noqa:E501
    quantization_config: Optional[QuantizationConfig] = Field(None, description="Quanization config") # noqa:E501, UP007
