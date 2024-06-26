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
        - `name` (str): name of the collection.
        - `vector_size` (str): JSON with names and sizes of vectors in the collection.
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

        If any element in `ids` is None, no other values will be passed.

    -----

    Args:
        messages (DF[CreateCollection]): A dataframe with names and parameters
        of the collections.
        ctx (Context[QdrantCreation]): context.

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
        raise Exception(f'Qdrant at `{client_url}` requires an API key') from exc

    df = {
        'status': []
    }
    collection_name = ctx.app_cfg.collection_name
    batch_size = ctx.app_cfg.batch_size
    parallel = ctx.app_cfg.parallel
    print(messages)
    vectors = [
        json.loads(message)
        for message in messages['vectors'].to_list()
    ]
    if {} in vectors or [] in vectors:
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
