from typing import Any

from jls import DF, jls


@jls.output(collection_name='saved_output')
def save_output(df: DF[Any]):
    print("Saved to collection `saved_output`")
    print(df.head())
