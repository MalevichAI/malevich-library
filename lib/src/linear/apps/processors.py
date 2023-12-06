from malevich.square import DF, Context, processor, scheme
from pydantic import BaseModel

from .linear import LinearExecutor


@scheme()
class GetProjectInputSchema(BaseModel):
    project_id: str


@processor()
def get_project(df: DF[GetProjectInputSchema], context: Context):
    """Get project by id

    Input:
        A dataframe with a column named `project_id` containing project id.

    Output:
        A dataframe with a column named `project` containing project.

    Args:
        df (DF[GetProjectInputSchema]):
            A dataframe with a column named `project_id` containing project id.

    Returns:
        DF[Project]:
            A dataframe with a column named `project` containing project.
    """
    linear: LinearExecutor = context.common
    outputs = []
    for _, row in df.iterrows():
        ...
        linear.create_issue(...)
        ...
    return outputs
