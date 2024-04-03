import pandas as pd
from malevich.square import Context, Sink, processor


@processor()
def concat(input: Sink, context: Context):
    """
    Concat DataFrames into one.

    ## Input:

    DataFrames you want to concat.

    ## Output:

    Concatenated DataFrame.

    -----
    Args:
        input (Sink): DataFrames you want to concat.
    Return:
        Concatenated DataFrame
    """
    data = []
    for i in input:
        data.append(i[0])

    return pd.concat(data, ignore_index=True)
