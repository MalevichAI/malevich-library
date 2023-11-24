from typing import Any

import pandas as pd
from malevich.square import DF, Context, processor


def _squash_df(df: pd.DataFrame, key: str, delm: str = ",") -> pd.DataFrame:
    data_ = {x: [" ".join(map(str, df[x].to_list()))] for x in df.columns if x != key}

    if key:
        data_[key] = [key]

    return pd.DataFrame(data_)


@processor()
def squash(df: DF[Any], context: Context):
    """Squash multiple rows into one row.

    Inputs:
        An arbitrary dataframe with columns that contain multiple values.

    Outputs:
        A dataframe with the same columns as the input dataframe, but with
        multiple rows for each input row.

    Configuration:
        by (str): The column to group by. If not specified, all
            columns will be squashed.

        delim (str): The delimiter used to separate values in the columns. If
            not specified, the default delimiter is a comma (,).

    Args:
        df (DF[Any]): Dataframe
        context (Context): Context object

    Returns:
        Dataframe with squashed rows
    """
    squash_by = context.app_cfg.get("by", None)
    squash_delim = context.app_cfg.get("delim", ",")

    if not squash_by:
        return _squash_df(df, squash_by, squash_delim)

    else:
        pds = []
        for name, group in df.groupby(squash_by):
            pds.append(_squash_df(group, name, squash_delim))
        return pd.concat(pds)
