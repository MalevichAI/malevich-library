from malevich.square import scheme, processor, DFS, DF, Context, Sink
import numpy as np
import pandas as pd
from pydantic import BaseModel
from .models import QueryConfig
import duckdb


@scheme()
class ExecuteMessage(BaseModel):
    query: str


@scheme()
class ExecuteTableNames(BaseModel):
    name: str


@processor()
def execute(
    messages: DF[ExecuteMessage],
    table_names: DF[ExecuteTableNames],
    tables: Sink[DF],
    placeholders: DF,
    ctx: Context[QueryConfig]
) -> DFS:
    db_name = ctx.app_cfg.db_name
    read_only = ctx.app_cfg.read_only
    table_format = ctx.app_cfg.table_format

    table_dict: dict[str, DF] = {}
    results = []
    with duckdb.connect(database=db_name, read_only=read_only) as con:
        for table, name in zip(tables, table_names['name'].tolist()):
            table_dict[name] = table
            duckdb.register(name, table)

        for message, placeholder in zip(
            messages['query'].tolist(),
            placeholders.to_dict(orient='tight')['data']
        ):
            real_placeholder = [item for item in placeholder if np.isnan(item)]
            result = con.execute(message.format(**table_format), real_placeholder)
            results.append(result.fetch_df())
    return results
