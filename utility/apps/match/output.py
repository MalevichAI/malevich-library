from typing import Any

from malevich.square import DF, output


@output(collection_name='saved_output')
def save_output(df: DF[Any]):
    print("Saved to collection `saved_output`")
    print(df.head())
