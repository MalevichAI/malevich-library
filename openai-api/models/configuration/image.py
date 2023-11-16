from typing import Optional

from .base import Configuration


class ImageConfiguration(Configuration):
    quality: Optional[str] = 'standard'
    size: Optional[str] = None
    style: Optional[str] = None
