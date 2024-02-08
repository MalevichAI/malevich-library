import pandas as pd
import requests
from malevich.square import DF, Context, processor, scheme
from pydantic import BaseModel


@scheme()
class Links(BaseModel):
    link: str

@processor()
def asser_links(df: DF[Links], context: Context) -> pd.DataFrame:
    """
        Check if the links are valid (do not return error status codes)

    ## Input:
           A dataframe that contains columns:
                - link: link to be validated

    ## Output:
            The format of dataframe depends on the configuration provided.

            If `filter_links` set to True, the output will be a dataframe
            with a column named `link` containing valid links.

            Otherwise the output will be a dataframe with a column named
            `error` containing invalid links.

    ## Configuration:
        - filter_links(bool, optional): If set to True, will filter the dataframe and exclude invalid links. Default value is False

    ---

    Args:
        df (DF[Links]): A dataframe with a column named `link` containing links.

    Returns:
        If `filter_links` is true, returns a dataframe with a column named `links` containing valid links.
        Otherwise, returns a dataframe with a column named `error` containing invalid links

    """  # noqa: E501
    errors = []
    valids = []
    for link in df['link'].to_list():
        try:
            response = requests.get(link)
            if response.status_code < 400:
                valids.append(link)
            else:
                errors.append(link)
        except requests.exceptions.ConnectionError:
            errors.append(link)

    if not context.app_cfg.get('filter_links', False):
        return pd.DataFrame(errors, columns=['errors'])

    else:
        return pd.DataFrame(valids, columns=['link'])
