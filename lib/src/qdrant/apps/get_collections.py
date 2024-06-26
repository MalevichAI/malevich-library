import pandas as pd
from malevich.square import DF, Context, processor
from qdrant_client import QdrantClient

from .models import Qdrant


@processor()
def get_collections(
    ctx: Context[Qdrant]
) -> DF:
    '''Create a collection in Qdrant.

    ## Input:

        None.


    ## Output:

        A dataframe with column:
        - `collection` (str): Name of the collection.

    ## Configuration:

        - `url`: str.
            URL location of your Qdrant DB.
        - `api_key`: str, default None.
            API key of your Qdrant DB.
        - `timeout`: int, default None.
            Connection timeout in seconds.
        - `https`: bool, default None.
            Whether HTTPS connection is used.

    -----

    Args:
        ctx (Context[Qdrant]): context.

    Returns:
        A dataframe of return statuses.
    '''

    client_url = ctx.app_cfg.url
    client_api_key = ctx.app_cfg.api_key
    client_timeout = ctx.app_cfg.timeout
    client_https = ctx.app_cfg.https
    try:
        qdrant_client = QdrantClient(
            url=client_url,
            api_key=client_api_key,
            timeout=client_timeout,
            https=client_https
        )
    except Exception as exc:
        raise Exception(f'Could not connect to `{client_url}`') from exc

    df = {
        'collections': []
    }
    for collection in qdrant_client.get_collections().collections:
        df['collections'].append(collection.name)

    return pd.DataFrame(df)
