import json

import pandas as pd
from malevich.square import DF, Context, processor, scheme
from qdrant_client import QdrantClient

from .models import Filter, Query


@scheme()
class ScrollMessage:
    filter: str
    limit: int

@scheme()
class ScrollResponse:
    query_id: int
    point_id: str | int
    payload: str
    vectors: str

@processor()
def scroll(
    messages: DF[ScrollMessage],
    ctx: Context[Query]
) -> DF[ScrollResponse]:
    '''Select points from a collection in Qdrant.

    ## Input:

        A dataframe consisting of columns:
        - `filter` (dict[str]): Qdrant filters packed into dictionary
        - `limit` (int): max responses returned

    ## Output:

        A dataframe with columns:
        - `query_id` (int): index of the query in the input DF
        - `point_id` (str | int): index of the point in Qdrant
        - `payload` (str): columns with payload keys.
        Number of columns depends on the payload.
        - `vectors` (str): columns with string representations of vectors.
        Number of columns depends on the payload.

    ## Configuration:

        - `` ():

    ## Note:

        No option for sort by and group by (yet).

    -----

    Args:
        messages (DF[ScrollMessage]): A dataframe with filters and limits.
        ctx (Context[Scroll]): context

    Returns:
        A dataframe with selected payloads and vectors.
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


    collection_name = ctx.app_cfg.collection_name
    with_vectors = ctx.app_cfg.with_vectors
    with_payload = ctx.app_cfg.with_payload

    df = {
        'query_id': [],
        'point_id': [],
        'payload': [],
        'vectors': []
    }

    for query_id, message in enumerate(messages.to_dict(orient='records')):

        try:
            results = qdrant_client.scroll(
                collection_name=collection_name,
                scroll_filter=Filter(**json.loads(message['filter'])),
                limit=message['limit'],
                with_payload=with_payload,
                with_vectors=with_vectors
            )
        except Exception:
            raise ValueError(
                '''`scroll` command failed!
                Try fixing `filter` column or check the config.
                ''')

        for result in results[0]:
            df['query_id'].append(query_id)
            df['point_id'].append(result.id)
            if result.payload:
                df['payload'].append(json.dumps(result.payload))
            else:
                df['payload'].append(None)
            if result.vector:
                df['vectors'].append(json.dumps(result.vector))
            else:
                df['vectors'].append(None)

    return pd.DataFrame(df)
