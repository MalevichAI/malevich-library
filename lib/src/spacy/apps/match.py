import string

import pandas as pd
from malevich.square import DF, Context, processor


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
def get_matches(
    text: DF,
    keys: DF,
    vals: DF,
    kvals: DF,
    context: Context
):
    """
    Match key-value in text

    ## Input:
    Four dataframes. First one is Text DataFrame with columns:
        - link (str): Aliexpress Link.
        - text (str): Aliexpress product info.
    ---

    Second one is Keys DataFrame with columns:
        - idx (int): Key ID.
        - key (str): Key name.

    ---

    Third one is Values DataFrame with columns:
        - idx (int): Value ID.
        - value (str): Value name.

    ---

    The last is match DataFrame which contains key -> value mapping.
        - key (int): Key ID.
        - value (int): Value ID.

    ## Output:
    Three DataFrames with results. First DataFrame contains matches.
        - link (str): Aliexpress link.
        - key (int): Key ID.
        - value (int): Value ID.
    ---
    Second one contains not matched keys.
        - link (str): Aliexpress link.
        - key (int): Key ID which wasn't found in the text.
    ---
    Third DF contains not matched values.
        - link (str): Aliexpress link.
        - key (int): Key ID which was found in the text.
        - value (int): Value ID which was not found.
    -----
    Args:
        text(DF): Text DataFrame.
        keys(DF): Keys DataFrame.
        values(DF): Values DataFrame.
        kvals(DF): Key-Values Mapping.
    Returns:
        Match results.
    """
    keys_dict = {}
    vals_dict = {}
    props = {}
    for _, row in keys.iterrows():
        keys_dict[row['idx']] = row['key']

    for _, row in vals.iterrows():
        vals_dict[row['idx']] = row['value']

    for kid in kvals['key'].unique():
        props[kid] = kvals[kvals['key'] == kid]['value'].to_list()

    matches = []
    not_matched_keys = []
    not_matched_value = []

    for _, row in text.iterrows():
        text_:str = row['text'].lower()
        for char in string.punctuation:
            if char in text_:
                text_ = text_.replace(char, ' ')

        for key in props.keys():
            if keys_dict[key].lower() not in text_:
                not_matched_keys.append([row['link'], key])
            else:
                for val in props[key]:
                    if vals_dict[val].lower() in text_:
                        matches.append([row['link'], key, val])
                    else:
                        not_matched_value.append(row['link'], key, val)
    return (
        pd.DataFrame(matches, columns=['link', 'key', 'value']),
        pd.DataFrame(not_matched_keys, columns=['link', 'key']),
        pd.DataFrame(not_matched_value, columns=['link', 'key', 'value'])
    )

@processor()
def get_matches_sm(text: DF, kvals: DF, context: Context):
    """
    Match key-value in text
    This is a simplified version of `get_matches`. It receives only 2 DataFrames and returns 1 with matched keys and values.
    ## Input:
    Two dataframes. First one is Text DataFrame with columns:
        - link (str): Aliexpress Link.
        - text (str): Aliexpress product info.
    ---

    Second one is Keys DataFrame with columns:
        - key (str): Key name.
        - value (str): Value name.

    ## Output:
    A DataFrames with matched keys and values.
        - link (str): Aliexpress link.
        - key (int): Key ID.
        - value (int): Value ID.

    ## Configuration:
        - squash_columns: bool, default False.
            Squash key, value columns into one column.
        - squash_result: str, default "key_value".
            Result column name.
        - squash_drop: bool, default False.
            Remove key, value columns.
        - squash_delim: str, default ",".
            Delimeter between key and value.
    -----
    Args:
        text(DF): Text DataFrame.
        kvals(DF): Key-Values Mapping.
    Returns:
        Match results.
    """  # noqa: E501
    props = {}
    for key in kvals['key'].unique():
        vals_ = kvals[kvals['key'] == key]['value'].to_list()
        props[key] = vals_

    matches = []
    not_matched_keys = []
    not_matched_value = []

    for _, row in text.iterrows():
        text_:str = row['text'].lower()
        for char in string.punctuation:
            if char in text_:
                text_ = text_.replace(char, ' ')

        for key in props.keys():
            if key.lower() not in text_:
                not_matched_keys.append([row['link'], key])
            else:
                for val in props[key]:
                    if val.lower() in text_:
                        matches.append([row['link'], key, val])
                    else:
                        not_matched_value.append(row['link'], key, val)

    matches = pd.DataFrame(matches, columns=['link', 'key', 'value'])
    if (len(matches) > 0 and context.app_cfg.get('squash_columns', False)):
        if context.app_cfg.get('squash_columns', False):
            matches = _squash_column_df(
                matches,
                ['key', 'value'],
                context.app_cfg.get("squash_result", None),
                context.app_cfg.get("squash_drop", False),
                context.app_cfg.get("squash_delim", ","),
            )

    return matches
