from malevich.square import processor


@processor()
def pass_through(df):
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

