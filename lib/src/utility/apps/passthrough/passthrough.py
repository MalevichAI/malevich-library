from malevich.square import DF, processor


@processor()
def pass_through(df: DF):
    return df
