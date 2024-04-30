from malevich.square import DF, Any, Context, processor

from .models import AddColumn


@processor()
def add_column(df: DF[Any], context: Context[AddColumn]):
    """Inserts a new column into a dataframe.

    ## Input:
        An arbitrary dataframe and context information
        with the following fields in the app config:
            column: name of the new column
            value: value of the new column
            position: position of the new column

    ## Output:
        The input dataframe with the new column inserted at the specified position.

    ## Details:
        The function takes in a dataframe as an input and adds a new column
        at the specified position. The new column has a constant value provided
        by the user in the application configuration.

        If the position is negative, the new column will be inserted from the
        end of the dataframe. For example, a position of -1 will insert the
        new column as the last column in the dataframe.

    ## Configuration:
        - column: str, default 'new_column'.
            The name of the new column.
        - value: any, default 'new_value'.
            The value of the new column.
        - position: int, default 0.
            The position to insert the new column. If positive, the new column will be inserted from the beginning of the dataframe. If negative, the new column will be inserted from the end of the dataframe.
        - skip_if_exists: bool, default False.
            If columns exists, no exception will be thrown if this flag is set.
    -----

    Args:
        df: The input dataframe.
        context: The context information.

    Returns:
        The dataframe with new column.
    """  # noqa: E501
    column_name = context.app_cfg.get('column', 'new_column')
    value = context.app_cfg.get('value', 'new_value')
    position = context.app_cfg.get('position', 0)

    if position < 0:
        position = len(df.columns) + position + 1

    if column_name in df.columns:
        if not context.app_cfg.skip_if_exists:
            raise ValueError(
                f"Collection already has a column {column_name}. You may "
                "specify to skip insertion in that case by providing "
                "`skip_if_exists=True` flag."
            )
    else:
        df.insert(position, column_name, value)

    return df


@processor()
def add_index(df: DF[Any], context: Context):
    """
    Add index column to the dataframe

    ## Input:

    Any dataframe

    ## Output:

    Input dataframe with additional column `index`

    -----
    Args:
        df (DF[Any]): Any dataframe
    Returns:
        Input dataframe with additional column `index`
    """
    df.reset_index(inplace=True)
    return df
