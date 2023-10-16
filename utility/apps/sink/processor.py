from typing import Any

from malevich.square import DF, processor


@processor()
def sink_two(df_1: DF[Any], df_2: DF[Any]):
    """Combine dataframes from different sources into a collection of dataframes.

    Input:
        Two dataframes of arbitrary types.

    Output:
        A collection of dataframes.

    Args:
        df_1: A dataframe of arbitrary type.
        df_2: A dataframe of arbitrary type.

    Returns:
        A collection of dataframes.
    """
    return df_1, df_2


@processor()
def sink_three(_d1: DF[Any], _d2: DF[Any], _d3: DF[Any]):
    """Combine dataframes from different sources into a collection of dataframes.

    Input:
        Three dataframes of arbitrary types.

    Output:
        A collection of dataframes.

    Args:
        _d1: A dataframe of arbitrary type.
        _d2: A dataframe of arbitrary type.
        _d3: A dataframe of arbitrary type.

    Returns:
        A collection of dataframes.
    """
    return _d1, _d2, _d3


@processor()
def sink_four(_d1: DF[Any], _d2: DF[Any], _d3: DF[Any], _d4: DF[Any]):
    """Combine dataframes from different sources into a collection of dataframes.

    Input:
        Four dataframes of arbitrary types.

    Output:
        A collection of dataframes.

    Args:
        _d1: A dataframe of arbitrary type.
        _d2: A dataframe of arbitrary type.
        _d3: A dataframe of arbitrary type.
        _d4: A dataframe of arbitrary type.

    Returns:
        A collection of dataframes.
    """
    return _d1, _d2, _d3, _d4


@processor()
def sink_five(_d1: DF[Any], _d2: DF[Any], _d3: DF[Any], _d4: DF[Any], _d5: DF[Any]):
    """Combine dataframes from different sources into a collection of dataframes.

    Input:
        Five dataframes of arbitrary types.

    Output:
        A collection of dataframes.

    Args:
        _d1: A dataframe of arbitrary type.
        _d2: A dataframe of arbitrary type.
        _d3: A dataframe of arbitrary type.
        _d4: A dataframe of arbitrary type.
        _d5: A dataframe of arbitrary type.

    Returns:
        A collection of dataframes.
    """
    return _d1, _d2, _d3, _d4, _d5