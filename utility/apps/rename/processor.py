from typing import Any

from malevich.square import DF, Context, processor


@processor()
def rename(df: DF[Any], context: Context):
    """Renames columns in a dataframe.

    Input:
        - DataFrame with the columns to be renamed.

    Configuration:
        - Provides mapping of old column names to their new names.

        For example, if the dataframe has columns 'a', 'b', 'c' and we want to rename
        'a' to 'A', 'b' to 'B', and 'c' to 'C', the configuration should be:

        {
            'a': 'A',
            'b': 'B',
            'c': 'C'
        }

    Details:
        This processor renames columns in the dataframe based on provided mappings.
        User needs to provide a dictionary in the configuration hat specifies old
        column names as keys and new column names as values.

    Args:
        df: DataFrame in which to rename columns.

    Returns:
        DataFrame with renamed columns.
    """
    return df.rename(columns=context.app_cfg)
