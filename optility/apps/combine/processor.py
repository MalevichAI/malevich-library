"""
This script contains functionalities to concatenate / combine vertically (on top of one another)
the outputs of different applications saved as Dataframe objects.
"""

import pandas as pd
from jls import jls, Context

# This list represents the expected arguments in the configuration of `combine_vertical` processor
__CV_FIELDS = ['ignore_col_names', 'default_name', 'ignore_index']

# some constants strings as a good practice
__COMBINE_V_ID = 'combine_vertical_id'
# the default name for columns
__DEFAULT_DEFAULT_NAME = 'col'


@jls.processor(id=__COMBINE_V_ID)
def combine_vertical(dataframe1: pd.DataFrame, dataframe2: pd.DataFrame, context: Context) -> pd.DataFrame:
    """
    The main purpose of this function is to combine / concatenate 2 dataframes (easily extendable to larger numbers)
    of dataframes while offering additional functionalities to customize the final output.

    Arguments:
    dataframe1, dataframe2 are self-explanatory
    context: represents the function's context and contains the needed configuration

    NOTE: the function raises a ValueError if the dataframes do not share the same number of columns

    The fields expected in the configuration:
    1. `ignore_col_names`: bool. Whether to ignore the current column names or not. In case of True
    The col names will be set to {default_name_i} where 'i' is the index of the column
    Defaults to False

    2. default_name: str: used to name columns with initially mismatched names, or when `ignore_col_names'
    is set to True. Defaults to 'col'

    3. ignore_index: bool: whether to ignore the index or not. Defaults to False

    The naming strategy is as follows:
    1. if `ignore_old_names` is set to True, then the new dataframe will have the generic names:
    `default_name_i` where `i` is the column's index

    2. if `ignore_old_names` is set to False, then the new dataframe will have the shared columns at
    first, and then those columns with mismatched names named as `default_name_i`
    where `i` starts from the column (N + 1) where N is the number of shared columns
    """

    # check the condition of equal number of columns
    if len(dataframe1.columns) != len(dataframe2.columns):
        raise ValueError("The 2 dataframes are expected to share the same number of columns")

    # extract the configuration
    # the if statement to run the function both with and without Malevish backend
    if isinstance(context, Context):
        config = context.app_cfg
    else:
        config = context

    # extract the arguments
    ignore_col_names = config.get(__CV_FIELDS[0], False)
    default_col_name = config.get(__CV_FIELDS[1], __DEFAULT_DEFAULT_NAME)
    ignore_index = config.get(__CV_FIELDS[2], False)

    new_df = pd.concat([dataframe1, dataframe2], axis=0, ignore_index=ignore_index)

    if ignore_col_names:
        # set the names to the generic naming
        new_df.columns = [f'{default_col_name}_{i}' for i, _ in enumerate(new_df.columns)]
        return new_df

    df1_col_names = set(dataframe1.columns.tolist())
    df2_col_names = set(dataframe2.columns.tolist())
    shared_col_names = df1_col_names.intersection(df2_col_names)

    cols = new_df.columns.tolist()
    # the idea here is to simply x
    # the idea here is to sort the column names using shared_col_names and their index in the original df
    sorted_col_names = sorted(cols,
                              key=lambda x: (x in shared_col_names, -dataframe1.columns.tolist().index(x)
                                             if x in df1_col_names else float('-inf'),
                                             ),
                              reverse=True)

    # set the mismatched columns to generic names

    for index in range(len(shared_col_names), len(df1_col_names)):
        sorted_col_names[index] = f'{default_col_name}_{index + 1}'

    res_df = new_df.reindex(columns=sorted_col_names[:len(df1_col_names)])
    return res_df
