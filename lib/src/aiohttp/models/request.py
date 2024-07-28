from malevich.square import scheme

from pydantic import BaseModel, Field
from typing import Optional

@scheme()
class RequestScheme(BaseModel):
    request: str
    path_kwargs: dict | None
    body: dict | None
    query: dict | None
    headers: dict | None

@scheme()
class Requests(BaseModel):
    requests: list[RequestScheme]

@scheme()
class ResponseScheme(BaseModel):
    responses: list[dict] | dict