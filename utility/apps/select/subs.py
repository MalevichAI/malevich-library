import re
from typing import Any

from jls import DFS, Context, M, jls


@jls.processor(id='subset')
def subset(dfs: DFS[M[Any]], context: Context):
    """Select a subset of dataframes from the list of dataframes.

    Input:
        A number of dataframes.

    Output:
        A subset of dataframes or a single dataframe.

    Configuration:
        expr: str
            A comma-separated list of integers or slices, e.g. `0,1:3,5:7,6,9:10`.
            The first dataframe has index 0.

    Details:
        The `expr` field should be a comma-separated list of integers or slices,
        e.g. `0,1:3,5:7,6,9:10`.

        Zero-based indexing is used for the dataframes.

        `expr` is matched against the regular expression
            `^(\d+|(\d+\:\d+))(\,(\d+|(\d+\:\d+)))*$`.

        If the expression contains only one element, a single dataframe is
        returned. Otherwise, a slice of dataframes is returned.

    Args:
        dfs: A number of arbitrary dataframes.

    Returns:
        A subset of dataframes or a single dataframe if the subset contains
        a single index.
    """
    # Parse `expr` field of the configuration
    expr = context.app_cfg.get("expr", None)
    if expr is None:
        raise ValueError("The app configuration should contain `expr` field")

    assert re.match(r"^(\d+|(\d+\:\d+))(\,(\d+|(\d+\:\d+)))*$", expr), \
        "The `expr` field should be a comma-separated list of integers " \
        "or slices, e.g. `0,1:3,5:7,6,9:10`"

    # Split the expression by comma
    exprs = expr.split(",")

    # Initialize the result
    result = []

    # Iterate over the expressions
    for expr in exprs:
        # Split the expression by colon
        expr = expr.split(":")

        # If the expression contains only one element,
        # it means that we should retrieve only one dataframe
        if len(expr) == 1:
            result.append(dfs[0][int(expr[0])])
        # Otherwise, we should retrieve a slice of dataframes
        else:
            result.extend(dfs[0][int(expr[0]):int(expr[1])])

    if len(result) == 1:
        return result[0]

    return result
