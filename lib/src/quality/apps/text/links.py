import pandas as pd
import requests
from malevich.square import DF, Context, processor, scheme
from pydantic import BaseModel


@scheme()
class Links(BaseModel):
    link: str

@processor()
def asser_links(df: DF[Links], context: Context):
    """
        Check if the links are valid (do not return error status codes)

        Input:
          DF[Links] - DataFrame with one column named 'link'.

        Output:
          DF[Links] - DataFrame with one column named 'link' containing
          valid or invalid links depending on 'filter_links' option.

        Options:
          filter_links - If True, returns links which passed assert. Else return
          error links.
    """
    errors = []
    valids = []
    for link in df['link'].to_list():
        try:
            status = requests.get(link)
            if status.status_code < 400:
                valids.append(link)
            else:
                errors.append(link)
        except requests.exceptions.ConnectionError:
            errors.append(link)

    if not context.app_cfg.get('filter_links', False):
        return pd.DataFrame(errors, columns=['link'])

    else:
        return pd.DataFrame(valids, columns=['link'])
