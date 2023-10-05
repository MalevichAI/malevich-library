from jls import jls, Context, DF
from typing import Any


@jls.processor()
def rename_column(df: DF[Any], context: Context):
    """Rename column in dataframe.
    
    To control the behavior of the processor, you should put mapping 
    into a context with original names as keys and desired names as values.
    
    For example:
        context.app_cfg = {
            "old_name": "new_name",
            "another_old_name": "another_new_name"
        }
    """
    return df.rename(columns=context.app_cfg)
