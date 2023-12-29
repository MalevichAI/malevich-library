import pandas as pd
from malevich.square import DF, Context, processor, scheme
from pydantic import BaseModel

from .parser import report_to_df


@scheme()
class XroadReport(BaseModel):
    filename: str

@processor()
def get_streets(df: DF[XroadReport], context: Context):
    """
    Get streets names from xroad reports

    Input:
        DataFrame with column 'filename' containing filenames of the reports

    Output:
        DataFrame with a column 'name' containing the name of streets from the report

    Args:
        DataFrame with column 'filename' containing filenames of the reports

    Returns:
        DataFrame with column 'filename' containing filenames of the reports
    """
    result_df = report_to_df(df, context)
    names = result_df['name'].unique()
    return pd.DataFrame(names, columns=['name'])
