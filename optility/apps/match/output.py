from jls import jls, DF
from typing import Any


@jls.output(collection_name='saved_output')
def save_output(df: DF[Any]):
    print("Saved to collection `saved_output`")
    print(df.head())