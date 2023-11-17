from typing import Optional

from .base import Configuration


class ImageConfiguration(Configuration):
    mode: str = 'image'
    quality: Optional[str] = 'standard'
    size: Optional[str] = None
    style: Optional[str] = None
