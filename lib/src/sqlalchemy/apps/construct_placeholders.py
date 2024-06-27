import pandas as pd
from malevich.square import DF, Context, processor

from .models import Placeholder


@processor()
def construct_placeholder(
    ctx: Context[Placeholder]
) -> DF:
    '''
    Helper processor for making placeholder dataframes. Aims to ease the use of the placeholders in `executemany()`


    ## Input:

        None.

    ## Output:

        A dataframe with columns:

        - `cmd_id` (int): id of the command.
        - `token` (str): placeholder token.
        - `value` (any): placeholder value.


    ## Configuration:

        - `tokens`: dict.
        Placeholders for each command in a JSON-like format.


    ## Notes:

        Example placeholder config:
        ```
        {
            0: {
                'plh_1': ['val_1', 'val_2', ...],
                ...,
                'plh_2': [0, 1, ...]
            },
            ...
        }
        ```
        IMPORTANT: for each command, the lists of placeholders should have the same length.

    -----

    Args:

        exec_msg (DF[ExecuteMessage]): dataframe with commands
        fmt_msg (DF[FormatTokenMessage]): dataframe with format tokens

    Returns:

        DF[Any]: result of the query or the number of rows affected by a query
    ''' # noqa:E501
    plh_cfg = ctx.app_cfg.tokens
    df = {
        'cmd_id': [],
        'token': [],
        'value': []
    }

    for id, plh in plh_cfg.items():
        lens = set()
        for key, val in plh.items():
            lens.add(len(val))
            if len(lens) > 1:
                raise ValueError(f'Placeholder lists for command `{id}` are not the same length!') # noqa:E501
            df['cmd_id'].extend([id] * len(val))
            df['token'].extend([key] * len(val))
            df['value'].extend(val)

    result = pd.DataFrame(df)
    return result
