from typing import Optional

from .base import Configuration


class TextConfiguration(Configuration):
    temperature: float = 0.9
    max_tokens: int = 512
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    stop: list = []
    echo: bool = False
    stream: bool = False
    logprobs: int = None
    n: int = 1
    best_of: int = 1
    response_format: Optional[str] = None
    output_history: bool = False
    include_index: bool = False
