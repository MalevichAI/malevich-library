from typing import Optional

from pydantic import BaseModel


class Configuration(BaseModel):
    api_key: str
    model: str = 'gpt-3.5-turbo'
    organization: Optional[str] = None
    max_retries: int = 3
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
    keep_index: bool = False
    keep_chat_index: bool = False
    keep_role: bool = False

