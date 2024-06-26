import pandas as pd
from malevich.square import DF, Context, processor, scheme
from qdrant_client import QdrantClient

from .models import Qdrant


@scheme()
class DeleteCollectionMessage:
    name: str

@scheme()
class DeleteCollectionResponse:
    status: bool

@processor()
def delete_collection(
    messages: DF[DeleteCollectionMessage],
    ctx: Context[Qdrant]
) -> DF[DeleteCollectionResponse]:
    '''Create a collection in Qdrant.


    ## Input:

        A dataframe consisting of columns:

        - `name` (str): Name of the collection.


    ## Output:

        A dataframe with column:

        - `status` (bool): Status of the operation. If True, collection was successfully created.


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
        messages (DF[DeleteCollectionMessage]): A dataframe with names and parameters
        of the collections.
        ctx (Context[Qdrant]): context.

    Returns:
        A dataframe of return statuses.
    '''  # noqa: E501

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
        'status': [],
    }
    for message in messages.to_dict(orient='records'):
        df['status'].append(
            qdrant_client.delete_collection(
                collection_name=message['name'],
            )
        )
    return pd.DataFrame(df)
