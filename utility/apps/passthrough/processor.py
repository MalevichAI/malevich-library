from jls import jls, DF, DFS, M
from typing import Any


@jls.processor()
def passthrough(df: DF[Any]):
    return df



@jls.processor()
def passthrough_many(dfs: DFS[M[Any]]):
    return dfs