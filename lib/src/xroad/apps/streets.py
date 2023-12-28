import pandas as pd
from checker import report_to_df
from malevich.square import DF, Context, processor, scheme
from pydantic import BaseModel


@scheme()
class XroadReport(BaseModel):
    filename: str

@processor()
def get_streets(df: DF[XroadReport], context: Context):
    result_df = report_to_df(df, context)
    names = result_df['name'].unique().to_list()
    return pd.DataFrame(names, columns=['name'])
