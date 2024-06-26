from typing import Any

import pandas as pd
from malevich.square import DF, Context, processor

from .models import Squash, SquashColumns, SquashRows


def _squash_row_df(
    df: pd.DataFrame, key: str, value: str, delm: str = ","
) -> pd.DataFrame:
    data_ = {
        x: [delm.join(map(str, df[x].to_list()))]
        for x in df.columns if x != key
    }

    if key:
        data_[key] = [value]

    return pd.DataFrame(data_)


def _squash_column_df(
    df: pd.DataFrame,
    columns: list[str] = None,
    res_col_name: str = None,
    drop: bool = False,
    delim: str = ",",
) -> pd.DataFrame:
    if not columns:
        columns = df.columns
    if not res_col_name:
        res_col_name = "_".join(columns)
    df_ = df.copy()
    # Turn all specified columns into strings
    df_[columns] = df_[columns].astype(str)
    if not df_.empty:
         df_[res_col_name] = df_[columns].apply(
             lambda row: delim.join(row), axis=1
        )
    if drop:
        df_.drop(columns=columns, inplace=True)
    return df_


@processor()
def squash_rows(df: DF[Any], context: Context[SquashRows]):
    """Squash multiple rows into one row.

    ## Input:
        An arbitrary dataframe with columns that contain multiple values.

    ## Output:
        A dataframe with the same columns as the input dataframe, but with
        multiple rows for each input row.

    ## Configuration:
        - `by`: str, default 'all'.
            The column to group by. If not specified, all columns will be squashed.

        - `delim`: str, default ','.
            The delimiter used to separate values in the columns. If not specified, the default delimiter is a comma (,).

    -----

    Args:
        df (DF[Any]): Dataframe
        context (Context): Context object

    Returns:
        Dataframe with squashed rows
    """  # noqa: E501
    squash_by = context.app_cfg.get("by", None)
    squash_delim = context.app_cfg.get("delim", ",")

    if not squash_by:
        return _squash_row_df(df, squash_by, squash_delim)

    else:
        pds = []
        for val, group in df.groupby(squash_by):
            pds.append(
                _squash_row_df(
                    group,
                    squash_by,
                    val,
                    squash_delim
                ).reset_index(drop=True)
            )
        if len(pds) != 0:
            return pd.concat(pds).reset_index(drop=True)
        else:
            return pd.DataFrame(columns=df.columns)


@processor()
def squash(df: DF[Any], context: Context[Squash]):
    """Squash multiple rows into one row.

    ## Input:
        An arbitrary dataframe with columns that contain multiple values.

    ## Output:
        A dataframe with the same columns as the input dataframe, but with
        multiple rows for each input row.

    ## Configuration:
        - `by`: str, default 'all'.
            The column to group by. If not specified, all columns will be squashed.

        - `delim`: str, default ','.
            The delimiter used to separate values in the columns. If not specified, the default delimiter is a comma (,).

    -----

    Args:
        df (DF[Any]): Dataframe
        context (Context): Context object

    Returns:
        Dataframe with squashed rows
    """  # noqa: E501
    return squash_rows(df, context)


@processor()
def squash_columns(df: DF[Any], context: Context[SquashColumns]):
    """Squash multiple columns into one column.

    ## Input:
        An arbitrary dataframe.

    ## Output:
        A dataframe with the same rows as the input dataframe, but with
        specified columns squashed into one column.

    ## Configuration:
        - `columns`: list[str], default None.
            The columns to squash. If not specified, all columns will be squashed.
        - `result_column_name`: str, default None.
            The name of the resulting column. If not specified, the default name is the concatenation of the column names.
        - `drop`: bool, default False.
            Whether to drop the original columns. If not specified, the default value is False.
        - `delim`: str, default ','.
            The delimiter used to separate values in the columns. If not specified, the default delimiter is a comma (,).

    -----

    Args:
        df (DF[Any]): An input collection
        config (Context): Configuration object

    Returns:
        Dataframe with squashed columns
    """  # noqa: E501
    return _squash_column_df(
        df,
        context.app_cfg.get("columns", None),
        context.app_cfg.get("result_column_name", None),
        context.app_cfg.get("drop", False),
        context.app_cfg.get("delim", ","),
    )
