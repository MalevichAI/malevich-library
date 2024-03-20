# Author: Leonid Zelenskiy <pak55256@gmail.com>
from itertools import product
from typing import Any

import pandas as pd
from malevich.square import DF, Context, processor

from .models import Unwrap


@processor()
def unwrap(
    df: DF[Any],
    context: Context[Unwrap]
):
    """Unwrap columns with multiple values into multiple rows.

    If a column contains multiple values, this processor will create a new row
    for each value. The new rows will be identical to the original row except
    for the column that was unwrapped.

    For example, if the input dataframe is:

    | id | name | tags |
    |----|------|------|
    | 1  | A    | a,b  |
    | 2  | B    | c    |

    Then the output dataframe will be:

    | id | name | tags |
    |----|------|------|
    | 1  | A    | a    |
    | 1  | A    | b    |
    | 2  | B    | c    |


    ## Input:

        An arbitrary dataframe with columns that contain multiple values.

    ## Output:

        A dataframe with the same columns as the input dataframe, but with
        multiple rows for each input row.

    ## Configuration:

        - `columns`: list[str], default ['all'].
            The columns to unwrap. If not specified, all columns will be unwrapped.

        - `delimiter`: str, default ','.
            The delimiter used to separate values in the columns. If not specified, the default delimiter is a comma (,).

    ## Notes:

        Be careful when using this processor with columns that contain
        non-text values. For example, if a column contains a list of numbers,
        and the delimiter is a dot, then the processor will treat each number
        as a separate value. For example, if the input dataframe is:

    | id | name | numbers |
    |----|------|---------|
    | 1  | A.B  | 1.2     |

        Then the output dataframe will be:

    | id | name | numbers |
    |----|------|---------|
    | 1  | A    | 1       |
    | 1  | A    | 2       |
    | 1  | B    | 1       |
    | 1  | B    | 2       |

    -----

    Args:

        df (pandas.DataFrame): The input dataframe.

        config (dict): The configuration for this processor.

    Returns:

        The same dataframe as the input dataframe, but with multiple rows for
        each input row.
    """  # noqa: E501

    pop_columns = context.app_cfg.get('columns', df.columns)
    delim = context.app_cfg.get('delimiter', ',')

    outputs = []

    for _, row in df.iterrows():
        outputs.extend(
            product(
                *[
                    (str(row[col]).split(delim) if col in pop_columns else [row[col]])
                    for col in df.columns
                ]
            )
        )

    return pd.DataFrame(outputs, columns=df.columns)
