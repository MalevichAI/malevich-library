from malevich.square import scheme, processor, DFS, DF, Context
from pydantic import BaseModel
from .models import Connection


@scheme()
class SelectMessage(BaseModel):
    name: str


@scheme()
class SelectResponse(BaseModel):
    status: str

@processor()
def select(
    create_message: DF[SelectMessage],
    *,
    context: Context[Connection]
) -> DF[SelectResponse]:
    ...

"""

df = select(data, condition(query1), on(query2))

"""