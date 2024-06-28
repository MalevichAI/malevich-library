import json

import pandas as pd
from malevich.square import DF, Context, processor, scheme
from qdrant_client import QdrantClient

from .models import Distance, Create


@scheme()
class CreateCollectionMessage:
    name: str
    on_disk: bool


@scheme()
class CreateCollectionResponse:
    status: bool


@processor()
def create_collection(
    messages: DF[CreateCollectionMessage],
    ctx: Context[Create]
) -> DF[CreateCollectionResponse]:
    '''Create a collection in Qdrant.


    ## Input:

        Consists of two dataframes:

        `messages` (DF[CreateCollectionMessage]): A dataframe with columns.
        - `name` (str): Name of the collection.
        - `on_disk` (bool): Read from disk instead of storing in memory.


    ## Output:

        A dataframe with column:

        - `status` (bool): Status of the operation. If `true`, collection was successfully created.


    ## Configuration:

        - `url`: str.
            URL location of your Qdrant DB.
        - `vectors`: dict.
            Vector size parameters.
        - `api_key`: str, default None.
            API key of your Qdrant DB.
        - `timeout`: int, default None.
            Connection timeout in seconds.
        - `https`: bool, default None.
            Whether HTTPS connection is used.
        - `hnsw_config`: dict, default None.
            HNSW config.
        - `optimizer_config`: dict, default None.
            Optimizer config.
        - `wal_config`: dict, default None.
            WAL config.
        - `quantization_config`: dict, default None.
            Quantization config.

    ## Notes:

        IMPORTANT! We strongly insist on giving name to vectors.
        It would be much easier to manage collections this way.

    -----

    Args:
        messages (DF[CreateCollectionMessage]): A dataframe with names and parameters
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
        'status': []
    }

    vectors = ctx.app_cfg.vectors
    hnsw_config = ctx.app_cfg.hnsw_config
    optimizers_config = ctx.app_cfg.optimizers_config
    wal_config = ctx.app_cfg.wal_config
    quantization_config = ctx.app_cfg.quantization_config

    for message in messages.to_dict(orient='records'):
        try:
            df['status'].append(
                qdrant_client.create_collection(
                    collection_name=message['name'],
                    vectors_config=vectors,
                    hnsw_config=hnsw_config,
                    optimizers_config=optimizers_config,
                    wal_config=wal_config,
                    quantization_config=quantization_config,
                    on_disk_payload=message['on_disk'],
                )
            )
        except Exception as exc:
            raise Exception(
                f'''
                Failed to create collection `{message["name"]}`
                '''
            ) from exc
    return pd.DataFrame(df)
