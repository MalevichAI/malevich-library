import json

import pandas as pd
from malevich.square import DF, Context, processor, scheme
from qdrant_client import QdrantClient

from .models import Update


@scheme()
class UploadCollectionMessage:
    vectors: str
    payload: str | None
    id: int | str | None

@scheme()
class UploadCollectionResponse:
    status: bool

@processor()
def upload_collection(
    messages: DF[UploadCollectionMessage],
    ctx: Context[Update]
) -> DF[UploadCollectionResponse]:
    '''Upload points in Qdrant.

    ## Input:

        A dataframe consisting of columns:
        - `vectors`: str
            JSON string of the vectors.
        - `payload`: str or None
            JSON string of the payload.
        - `id`: int or str or None
            Distance score metric (case insensitive). Available metrics: `cosine`, `dot`, `manhattan`, `euclid`

    ## Output:

        A dataframe with column:
        - `status`: bool
            Status of the operation. If True, collection was successfully created.

    ## Configuration:

        - `url`: str
            URL location of your Qdrant DB
        - `api_key`: str or None
            API key of your Qdrant DB
        - `timeout`: int or None
            Connection timeout in seconds
        - `https`: bool or None
            Whether HTTPS connection is used


    ## Notes:

        If any element in `ids` is None, no other values will be passed.

    -----

    Args:
        messages (DF[UploadCollectionMessage]): A dataframe with names and parameters of the collections.
        ctx (Context[Update]): context.

    Returns:
        A dataframe of return statuses.
    ''' # noqa:E501

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
        'status': []
    }
    collection_name = ctx.app_cfg.collection_name
    batch_size = ctx.app_cfg.batch_size
    parallel = ctx.app_cfg.parallel
    vectors = [
        json.loads(message)
        for message in messages['vectors'].to_list()
    ]
    if not all(vectors):
        raise Exception('Please set at least one of the vectors to a correct value for every point') # noqa:E501
    payloads = [
        json.loads(message) if isinstance(message, str) else None
        for message in messages['payload'].to_list()
    ]
    if payloads.count(None) > 0:
        if payloads.count(None) == len(payloads):
            payloads = None
        else:
            raise Exception('Please set all of the `payload` either to None or to a correct JSON string') # noqa:E501
    ids = [
        message if not isinstance(message, float) else None
        for message in messages['id'].to_list()
    ]
    # If one of the ids is None, we should not pass any
    # since it would break `upload_collection`
    if ids.count(None) > 0:
        if ids.count(None) == len(ids):
            ids = None
        else:
            raise Exception('Please set all of the `id` either to None or to a correct id') # noqa:E501
    try:
        qdrant_client.upload_collection(
            collection_name=collection_name,
            vectors=vectors,
            payload=payloads,
            ids=ids,
            batch_size=batch_size,
            parallel=parallel
        )
    except Exception as exc:
        raise Exception(f'Upload to collection `{collection_name}` failed!') from exc # noqa:E501

    return pd.DataFrame(df)
