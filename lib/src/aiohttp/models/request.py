from malevich.square import scheme

from pydantic import BaseModel, Field
from typing import Optional

@scheme()
class RequestScheme(BaseModel):
    request: str
    path_kwargs: dict | None = None
    body: dict | None = None
    query: dict | None = None
    headers: dict | None = None

@scheme()
class Requests(BaseModel):
    requests: list[RequestScheme]

@scheme()
class ResponseScheme(BaseModel):
    responses: list[dict] | dict