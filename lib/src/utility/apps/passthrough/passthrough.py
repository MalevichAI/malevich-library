from malevich.square import DF, processor


@processor()
def pass_through(df: DF):
    """
    Passes df to the next app

    ## Input:

        Arbitrary DataFrame

    ## Output:

        Arbitrary DataFrame

    -----
    Args:
        df (DF): Arbitrary DataFrame
    Returns:
        df (DF): Arbitrary DataFrame
    """
    return df

