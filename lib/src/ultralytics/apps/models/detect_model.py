# generated by datamodel-codegen:
#   filename:  detect_model.json
#   timestamp: 2024-03-23T14:20:37+00:00

from __future__ import annotations

from typing import Any, Optional

from malevich.square import scheme
from pydantic import BaseModel, Field


@scheme()
class Detect(BaseModel):
    weights: Optional[str] = Field(
        'yolo.pt', description='A path to the weights file in the shared storage'
    )
    conf: Optional[float] = Field(0.25, description='Confidence threshold')
    iou: Optional[float] = Field(0.45, description='IoU threshold')
    classes: Optional[dict[str, Any]] = Field(
        {}, description='A dictionary that maps class ids to class names'
    )
    save_plots: Optional[bool] = Field(
        False, description='Whether to save the output images'
    )
    save_path: Optional[str] = Field(
        'default', description='The pattern for the path to the output images'
    )
    batch_size: Optional[int] = Field(1, description='The batch size')
