import json
import pandas as pd
from malevich.square import DF, Context, processor, scheme
from qdrant_client import QdrantClient

from .models import Distance, Qdrant, VectorParams


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
        - `name` (str): name of the collection.
        - `vector_size` (str): JSON string of names and sizes of vectors in the collection.
        - `distance` (str): distance score metric (case insensitive).
        Available metrics: `cosine`, `dot`, `manhattan`, `euclid`

    ## Output:

        A dataframe with column:
        - `status` (bool): status of the operation. If `true`, collection was
        successfully created.

    ## Configuration:

        - `url` (str): URL location of your Qdrant DB
        - `api_key` (str | None): API key of your Qdrant DB

    ## Notes:

        IMPORTANT! We strongly insist on giving name to vectors.
        It would be much easier to manage collections this way.

    -----

    Args:
        messages (DF[CreateCollection]): A dataframe with names and parameters
        of the collections.
        ctx (Context[QdrantCreation]): context.

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
        raise Exception(f'Qdrant at `{client_url}` requires an API key') from exc

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
