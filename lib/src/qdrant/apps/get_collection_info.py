import pandas as pd
from malevich.square import DF, Context, processor, scheme
from qdrant_client import QdrantClient

from .models import Qdrant


@scheme()
class GetCollectionInfoMessage:
    name: str

@scheme()
class GetCollectionInfoResponse:
    info: str

@processor()
def get_collection_info(
    messages: DF[GetCollectionInfoMessage],
    ctx: Context[Qdrant]
) -> DF[GetCollectionInfoResponse]:
    '''Create a collection in Qdrant.

    ## Input:

        A dataframe consisting of columns:
        - `name` (str): name of the collection.

    ## Output:

        A dataframe with column:
        - `info` (str): JSON string with the info about the collection.

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
        messages (DF[GetCollectionInfo]): A dataframe with names and parameters
        of the collections.
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
        'info': []
    }
    for message in messages.to_dict(orient='records'):
        df['info'].append(
            qdrant_client.get_collection(
                collection_name=message['name'],
            ).model_dump_json()
        )
    return pd.DataFrame(df)
