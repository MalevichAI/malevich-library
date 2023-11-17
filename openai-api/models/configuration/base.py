from typing import Optional

from pydantic import BaseModel


class Configuration(BaseModel):
    api_key: str
    mode: Optional[str] = None
    model: str = 'gpt-3.5-turbo'
    organization: Optional[str] = None
    max_retries: int = 3
    include_index: bool = False
