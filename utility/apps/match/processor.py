"""
This script contains the processor code for the pattern matching functionality

This is an implementation of the 1.2 proposal as explained in the following document:
https://www.craft.me/s/NmXjF6pbB5m0BG (might require logging in with email...)
"""

import re

import pandas as pd
from malevich.square import DF, Context, processor

__PATTERN_MATCH_ID = 'pattern_match_processor'
__MP_FIELDS = ['pattern', 'join_char']
__DEFAULT_JOIN_CHAR = ';'


def _find_all_matches(text: str,
                      pattern: str,
                      join_str: str) -> str:
    matches = re.finditer(pattern=pattern, string=text)
    # extract the actual text using the indices found in each match object
    matches = [text[match_obj.span()[0]: match_obj.span()[1]] for match_obj in matches]
    return join_str.join(matches)


@processor(id=__PATTERN_MATCH_ID)
def match_pattern(dataframe: DF, context: Context) -> pd.DataFrame:
    """
    This processor finds all the fragments that match a certain pattern within each cell.
    They are later joined with a certain symbol and saved in an analogue cell

    Args:
        dataframe: the input
        context: the usual Malevich context, we expect the field 'pattern' from it.

    Returns: a new dataframe with the same dimensions and names as the input dataframe.
    """
    config = context.app_cfg

    # pattern is required
    pattern = config.get(__MP_FIELDS[0])
    # the join_char is optional
    join_char = config.get(__MP_FIELDS[1], __DEFAULT_JOIN_CHAR)

    # first determine which types can be inferred as string types
    str_columns = [c for c in dataframe.columns if pd.api.types.is_string_dtype(dataframe[c])]

    def match_pattern_map_function(row):
        for c in str_columns:
            row[c] = _find_all_matches(text=row[c],
                                       pattern=pattern,
                                       join_str=join_char)

            # make sure the cell is set to an empty string and not a None value
            row[c] = "" if row[c] is None else row[c]

        return row

    result = dataframe.apply(match_pattern_map_function, axis=1)

    # make sure the operation did not change the dataframe's dimensions
    assert tuple(result.shape) == tuple(dataframe.shape)

    return result
