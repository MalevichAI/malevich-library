from malevich.square import scheme, processor, DFS, DF, Context
from pydantic import BaseModel
from .models import Connection


@scheme()
class OnMessage(BaseModel):
    name: str


@scheme()
class OnResponse(BaseModel):
    status: str

@processor()
def on(
    message: DF[OnMessage],
    *,
    context: Context[Connection]
) -> DF[OnResponse]:
    ...