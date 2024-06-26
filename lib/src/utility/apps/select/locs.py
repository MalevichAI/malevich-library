from typing import Any

import pandas as pd
from malevich.square import DF, Context, processor

from .models import Locs


@processor(id='locs')
def locs(df: DF[Any], context: Context[Locs]):
    """ Locate Statically - Extracts a subset of the dataframe

    ## Input:
        A DataFrame to be processed.

    ## Output:
        A DataFrame with requested columns

    ## Configuration:
        The app configuration should contain at least one of the following fields:

        - `column`: str, default None.
          The column to be extracted.
        - `columns`: list[str], default None.
          The columns to be extracted.
        - `column_idx`: int, default None.
            The column index to be extracted.
        - `column_idxs`: list[int], default None.
            The column indexes to be extracted.
        - `row`: int, default None.
            The row to be extracted.
        - `rows`: list[int], default None.
            The rows to be extracted.
        - `row_idx`: int, default None.
            The row index to be extracted.
        - `row_idxs`: list[int], default None.
            The row indexes to be extracted.
        - `unique`: bool, default False.
            Get unique values from column. Must be used with `column` or `column_idx`.

        Multiple fields may be provided and in such case,
        the function will extract the intersection of the fields.

    ## Notes:
        At least one of the above fields should be provided for the function to work.

        Moreover, the dataframe is processed in column first then row order.
        Queries are executed from the most specific to the least within each category.
        If both specific and general conditions are given, the function prioritizes
        the specific ones to maintain consistency.

    -----

    Args:
        df (pd.DataFrame): The DataFrame to be processed.

    Returns:
        The extracted subset from the DataFrame.
    """
    should_have = ['column', 'columns', 'column_idx', 'column_idxs',
                     'row', 'rows', 'row_idx', 'row_idxs']


    if not any([field in context.app_cfg for field in should_have]):
        raise ValueError(
            f'At least one of the following fields should be provided: {should_have}'
        )


    # Extract the fields from the context object
    # to make the code more readable and avoid
    # multiple calls to the context object

    column = context.app_cfg.get('column', None)
    columns = context.app_cfg.get('columns', None)
    column_idx = context.app_cfg.get('column_idx', None)
    column_idxs = context.app_cfg.get('column_idxs', None)
    row = context.app_cfg.get('row', None)
    rows = context.app_cfg.get('rows', None)
    row_idx = context.app_cfg.get('row_idx', None)
    row_idxs = context.app_cfg.get('row_idxs', None)
    unique = context.app_cfg.get('unique', False)

    if unique and not (column or column_idx):
        raise AssertionError("unique field should be used with column or column_idx")

    # Copy the dataframe to avoid side effects
    result: pd.DataFrame = df.copy()

    # ________________________________________________


    # We start with column id as it is the most specific
    # and thus the most restrictive
    if column_idx is not None and len(result.columns) > column_idx:
        series = result.iloc[:, column_idx]
        if unique:
            result = pd.DataFrame(pd.unique(series), columns=[series.name])
        else:
            result = pd.DataFrame(series)
    elif column_idxs is not None:
        # Multiple indices are only processed if
        # column_id is not provided to keep
        # indices consistent

        # Filter only those indices that are in the dataframe
        # to tolerate missing columns
        column_idxs = [
            idx for idx in column_idxs
            if len(result.columns) > idx
        ]

        result = pd.DataFrame(result.iloc[:, column_idxs])


    # ________________________________________________


    if column is not None and column in result.columns:
        series: pd.Series = result[column]
        if unique:
            result = pd.DataFrame(pd.unique(series), columns=[series.name])
        else:
            result = pd.DataFrame(series)
        result = pd.DataFrame(result[column])

    if columns is not None:
        # Multiple columns are only processed if
        # column is not provided to keep
        # indices consistent

        # Filter only those columns that are in the dataframe
        # to tolerate missing columns
        columns = [
            col for col in columns
            if col in result.columns
        ]

        result = pd.DataFrame(result[columns])


    # ________________________________________________

    # We continue with row id as it is the most specific
    # and thus the most restrictive

    if row_idx is not None and len(result) > row_idx:
        result = pd.DataFrame(result.iloc[[row_idx], :])
    elif row_idxs is not None:
        # Multiple indices are only processed if
        # row_id is not provided to keep
        # indices consistent

        # Filter only those indices that are in the dataframe
        # to tolerate missing rows
        row_idxs = [
            idx for idx in row_idxs
            if len(result) > idx
        ]

        result = pd.DataFrame(result.iloc[row_idxs, :])


    # ________________________________________________

    if row is not None and row in result.index:
        result = pd.DataFrame(result.loc[[row]])

    if rows is not None:
        # Multiple rows are only processed if
        # row is not provided to keep
        # indices consistent

        # Filter only those rows that are in the dataframe
        # to tolerate missing rows
        rows = [
            row for row in rows
            if row in result.index
        ]

        result = pd.DataFrame(result.loc[rows])

    if context.app_cfg.get('print', False):
        print(result.head())

    return pd.DataFrame(result)


