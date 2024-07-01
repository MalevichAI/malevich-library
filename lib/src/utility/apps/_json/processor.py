import json

import pandas as pd
from malevich.square import DF, Context, processor

from .models import ChangeJson


@processor()
def change_json(df: DF, ctx: Context[ChangeJson]):
    """
    Retrieve values by path.

    ## Input:
        A single DataFrame.

    ## Output:
        The same DataFrame with results.

    ## Configuration:
        - path: str.
            The path to follow in format "key1.key2.key3" .
        - raise_on_error: str, default True.
            Raise error if nothing was found by the path.
    -----
    """
    assert 'path' in ctx.app_cfg, "Must provide a path"
    path: str = ctx.app_cfg.get('path').split('.')
    error_raise = ctx.app_cfg.get('raise_on_error', True)
    res = {}
    for c, s in df.to_dict(orient='list').items():
        rows = []
        for row in s:
            if isinstance(row, str):
                try:
                    data = json.loads(row)
                    for key in path:
                        if isinstance(data, list):
                            try:
                                key = int(key)
                            except Exception:
                                pass
                        try:
                            data = data[key]
                        except Exception as e:
                            if error_raise:
                                raise e
                            else:
                                raise json.JSONDecoder
                    rows.append(
                        json.dumps(data) if isinstance(data, (dict, list)) else data
                    )
                except json.JSONDecodeError:
                    rows.append(row)
                    continue
            else:
                rows.append(row)
                continue
        res[c] = rows

    return pd.DataFrame(res)
