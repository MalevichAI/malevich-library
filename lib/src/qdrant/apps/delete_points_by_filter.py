import json

import pandas as pd
from malevich.square import DF, Context, processor, scheme
from qdrant_client import QdrantClient

from .models import Delete, Filter


@scheme()
class DeleteCollectionFilterMessage:
    filter: str


@scheme()
class DeleteCollectionResponse:
    status: str


@processor()
def delete_points_by_filter(
    messages: DF[DeleteCollectionFilterMessage],
    ctx: Context[Delete]
) -> DF[DeleteCollectionResponse]:
    '''Create a collection in Qdrant.

    ## Input:

        A dataframe consisting of columns:
        - `filter`: str
            JSON string of the filter for deletion.

    ## Output:

        A dataframe with column:
        - `status`: str
            Status of the operation.

    ## Configuration:

        - `url`: str
            URL location of your Qdrant DB
        - `api_key`: str or None
            API key of your Qdrant DB
        - `timeout`: int or None
            Connection timeout in seconds
        - `https`: bool or None
            Whether HTTPS connection is used
        - `collection_name`: str or None
            Name of the collection
        - `ordering`: str or None
            JSON string with the ordering of the deletion

    -----

    Args:
        messages (DF[DeleteCollectionFilterMessage]): A dataframe with names and parameters
        of the collections.
        ctx (Context[Delete]): context.

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
    collection_name = ctx.app_cfg.collection_name
    ordering = ctx.app_cfg.ordering
    for message in messages.to_dict(orient='records'):
        try:
            df['status'].append(
                str(
                    qdrant_client.delete(
                        collection_name=collection_name,
                        points_selector=Filter(**json.loads(message['filter'])),
                        ordering=ordering
                    ).status
                )
            )
        except Exception as exc:
            raise Exception(
                'Failed to delete points.'
            ) from exc
    return pd.DataFrame(df)
