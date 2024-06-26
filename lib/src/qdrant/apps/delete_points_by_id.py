import pandas as pd
from malevich.square import DF, Context, processor, scheme
from qdrant_client import QdrantClient

from .models import Delete


@scheme()
class DeleteCollectionPointsMessage:
    id: str | int


@scheme()
class DeleteCollectionResponse:
    status: str


@processor()
def delete_points_by_id(
    messages: DF[DeleteCollectionPointsMessage],
    ctx: Context[Delete]
) -> DF[DeleteCollectionResponse]:
    '''Create a collection in Qdrant.

    ## Input:

        A dataframe consisting of columns:
        - `id` (str): Name of the collection.

    ## Output:

        A dataframe with column:
        - `status` (str): Status of the operation.

    ## Configuration:

        - `url`: str.
            URL location of your Qdrant DB.
        - `api_key`: str, default None.
            API key of your Qdrant DB.
        - `timeout`: int, default None.
            Connection timeout in seconds.
        - `https`: bool, default None.
            Whether HTTPS connection is used.
        - `collection_name`: str, default None.
            Name of the collection.
        - `ordering`: str, default None.
            JSON string with the ordering of the deletion.
    -----

    Args:
        messages (DF[DeleteCollectionPointsMessage]): A dataframe with names and parameters
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
    try:
        df['status'].append(
            str(
                qdrant_client.delete(
                    collection_name=collection_name,
                    points_selector=messages['id'].to_list(),
                    ordering=ordering
                ).status
            )
        )
    except Exception as exc:
        raise Exception(
            'Failed to delete points.'
        ) from exc
    return pd.DataFrame(df)
