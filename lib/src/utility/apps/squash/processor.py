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
    squash_by = context.app_cfg.get("by", None)
    squash_delim = context.app_cfg.get("delim", ",")

    if not squash_by:
        return _squash_df(df, squash_by, squash_delim)

    else:
        pds = []
        for name, group in df.groupby(squash_by):
            pds.append(_squash_df(group, name, squash_delim))
        return pd.concat(pds)
