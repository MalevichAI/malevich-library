import re
from typing import Optional, Union

import pandas as pd
from malevich.square import DF, Context, processor
from pydantic import BaseModel, ValidationError

from .models import AssertRegex


class Index(BaseModel):
    start: Optional[Union[int, float]] = None
    end: Optional[Union[int, float]] = None
    step: Optional[Union[int, float]] = None


class Rule(BaseModel):
    regex: Union[str, re.Pattern]
    column: Optional[Union[str, Index]] = None
    row: Optional[Union[str, Index]] = None
    invert: Optional[bool] = False
    message: Optional[str] = None


def _error_message(
    val: str,
    re_: re.Pattern,
    column: str,
    row: int,
    message: Optional[str] = None
) -> str:
    if message:
        return f"At column '{column}' and row {row}: {message}"
    else:
        return f"The value at column {column} and row {row} " \
            f"does not match pattern {re_.pattern}:\n {val[:50]}" \
            f"{'...' if len(val) > 50 else ''}"


@processor()
def assert_regex(df: DF, ctx: Context[AssertRegex]):
    """Asserts that the values in a dataframe match a regex.

    ## Input:
        An arbitrary dataframe.

    ## Output:
        A dataframe with a column:
        - `errors` (str): containing the errors if any.

    ## Configuration:
        - `rules`: list[dict], default [].
            The rules to apply.
        - `raise_on_error`: bool, default False.
            Whether to raise an exception if an error is found.

    ## Rules:
        A rule is a dictionary with the following keys:
            - regex (str): The regex to match the values against.
            - column (str or Index, default None): The column to apply the rule to.
                If None, the rule will be applied to all columns.
            - row (str or Index, default None): The row to apply the rule to.
                If None, the rule will be applied to all rows.
            - invert (bool, default False): Whether to invert the rule.
                If True, the rule will be applied to values that do not match
                the regex.

        An Index is a dictionary with the following keys:
            - start (int or float, default None): The starting index.
                If None, the starting index will be 0.
            - end (int or float, default None): The ending index.
                If None, the ending index will be the length of the dataframe.
            - step (int or float, default None): The step of the index.
                If None, the step will be 1.

        If a float is provided for the start, end, or step, the value will
        be interpreted as a percentage of the length of the dataframe.

    ## Example:

    {
        "rules": [
            {
                "regex": ".*",
                "column": "column1",
                "row": {
                    "start": 0.5,
                    "end": 1.0,
                    "step": 0.5
                },
                "invert": false
    }

    -----

    Args:
        df (DF):
            An arbitrary dataframe.
        ctx (Context):
            The context object.

    Returns:
        A dataframe with a column named `errors` containing the errors
        if any.

    Raises:
        Exception: If an error is found and `raise_on_error` is True.
    """
    rules = ctx.app_cfg.get('rules', [])
    raise_on_error = ctx.app_cfg.get('raise_on_error', False)
    try:
        rules = [
            Rule(**rule)
            for rule in rules
        ]
    except ValidationError as e:
        raise Exception(f'Invalid rule: {e}') from e

    for rule in rules:
        # Try to compile the regex
        try:
            re.compile(rule.regex)
        except re.error as e:
            raise Exception(f'Invalid regex: {e}') from e

        if rule.column is None:
            rule.column = Index(start=0., end=1.)
        if rule.row is None:
            rule.row = Index(start=0., end=1.)

        if rule.column is not None and isinstance(rule.column, Index):
            if isinstance(rule.column.start, float):
                rule.column.start = int(rule.column.start * len(df.columns))
            if isinstance(rule.column.end, float):
                rule.column.end = int(rule.column.end * len(df.columns))
            if isinstance(rule.column.step, float):
                rule.column.step = int(rule.column.step * len(df.columns))

        if rule.row is not None and isinstance(rule.row, Index):

            if isinstance(rule.row.start, float):
                rule.row.start = int(rule.row.start * len(df))
            if isinstance(rule.row.end, float):
                rule.row.end = int(rule.row.end * len(df))
            if isinstance(rule.row.step, float):
                rule.row.step = int(rule.row.step * len(df))

    errors = []

    for rule in rules:
        if rule.column is None:
            rule.column = Index(start=0., end=1.)
        if rule.row is None:
            rule.row = Index(start=0., end=1.)

    for rule in rules:
        slice_ = df
        re_ = re.compile(rule.regex)
        if isinstance(rule.column, Index):
            slice_ = slice_.iloc[:,
                                 rule.column.start:rule.column.end:rule.column.step]
        elif isinstance(rule.column, str):
            slice_ = slice_[rule.column]

        if isinstance(rule.row, Index):
            slice_ = slice_.iloc[rule.row.start:rule.row.end:rule.row.step, :]
        elif isinstance(rule.row, str):
            slice_ = slice_.loc[rule.row, :]

        for col_ in slice_.columns:
            for i, val_ in enumerate(slice_[col_].to_list()):
                val_ = str(val_)
                try:
                    if not (re.match(re_, val_) is not None) ^ rule.invert:
                        if raise_on_error:
                            raise Exception(
                                _error_message(val_, re_, col_, i, rule.message)
                            )
                        else:
                            errors.append(
                                _error_message(val_, re_, col_, i, rule.message)
                            )
                except re.error:
                    if raise_on_error:
                        raise Exception(
                            _error_message(val_, re_, col_, i, rule.message)
                        )
                    else:
                        errors.append(_error_message(val_, re_, col_, i, rule.message))

    return pd.DataFrame(errors, columns=["errors"])
