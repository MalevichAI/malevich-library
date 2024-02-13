import pandas as pd
import requests
from malevich.square import DF, Context, processor, scheme
from pydantic import BaseModel


@scheme()
class Links(BaseModel):
    link: str

@processor()
def assert_links(df: DF[Links], context: Context) -> pd.DataFrame:
    """
        Check if the links are valid (do not return error status codes)

    ## Input:
        A dataframe that contains a column:
            - link: link to be validated

    ## Output:
        The format of dataframe depends on the configuration provided.

        If `filter_links` set to True, the output will be a dataframe
        with a column named `link` containing valid links.

        Otherwise the output will be a dataframe with a column named
        `error` containing invalid links.

    ## Configuration:
        - filter_links: bool, optional, default False.
            If set to True, will filter the dataframe and exclude invalid links.

    ---

    Args:
        df (DF[Links]): A dataframe with a column named `link` containing links.

    Returns:
        If `filter_links` is true, returns a dataframe with a column named `links` containing valid links.
        Otherwise, returns a dataframe with a column named `error` containing invalid links

    """  # noqa: E501
    outputs = []
    _filter = context.app_cfg.get('filter_links', False)
    for link in df['link'].to_list():
        try:
            response = requests.get(link, allow_redirects=True)
            print(f'Link: {link} status {response.status_code}')
            if (response.status_code < 400) == _filter:
                result = (
                    link
                    if _filter
                    else f"Received {response.status_code} from {link}"
                )
                outputs.append(result)

        except requests.exceptions.ConnectionError:
            if not _filter:
                outputs.append("Links does not exist."
                               "Probably it leads to an invalid domain (address)"
                               "or a service is down."
                )

    return pd.DataFrame(outputs, columns=['errors' if not _filter else 'link'])

