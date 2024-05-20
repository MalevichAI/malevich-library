from malevich.square import scheme
from pydantic import BaseModel, Field


@scheme()
class DetectVideo(BaseModel):
    conf: float | None = Field(0.25, description='Confidence threshold')
    iou: float | None=  Field(0.45, description='IoU threshold')
    classes: list[int] | None = Field(
        None,
        description="A list of classes to detect. By default predicts all classes"
    )
    gpus: list[int] | None = Field(
        None,
        description="List of GPU indices. If None, uses all available GPUs"
    )
    return_raw: bool = Field(
        False,
        description="If True, returns JSON-serialized YOLO Results objects"
    )
    save_images: bool = Field(
        True,
        description="Whether to save and original images across apps"
    )
    fps: int | None = Field(
        None,
        description="Frame per second for video processing"
    )
