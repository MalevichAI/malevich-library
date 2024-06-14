import json
import pandas as pd
from malevich.square import DF, Context, processor, scheme
from qdrant_client import QdrantClient

from .models import Distance, Qdrant, VectorParams


@scheme()
class CreateCollectionMessage:
    name: str
    vector_size: str
    distance: str
    on_disk: bool
    hnsw_config: str | None
    optimizer_config: str | None
    wal_config: str | None
    quantization_config: str | None


@scheme()
class CreateCollectionResponse:
    status: bool

@processor()
def create_collection(
    messages: DF[CreateCollectionMessage],
    ctx: Context[Qdrant]
) -> DF[CreateCollectionResponse]:
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

    def json_or_none(x) -> dict | None:
        """
        Helper function for loading JSON string or returning None
        """
        return json.loads(x) if isinstance(x, str) else None

    def get_enum(x: str) -> Distance:
        """
        Helper function for transforming strings into `Distance`
        enum from `qdrant_client.models`
        """
        # Generate a dict where
        # string representation is a key
        # and Distance object is a value
        keys = dict(
            map(
                lambda e: (str(e).lower(), e),
                list(Distance)
            )
        )
        if x.lower() not in keys:
            raise KeyError(f'"{x.lower()}" is not a valid distance score')
        return keys[x.lower()]


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
    for message in messages.to_dict(orient='records'):
        try:
            df['status'].append(
                qdrant_client.create_collection(
                    collection_name=message['name'],
                    vectors_config={
                        name : VectorParams(
                                size=size,
                                distance=get_enum(message['distance']),
                                on_disk=message['on_disk']
                            )
                        for name, size in json.loads(message['vector_size']).items()
                    },
                    hnsw_config=json_or_none(message['hnsw_config']),
                    optimizers_config=json_or_none(message['optimizer_config']),
                    wal_config=json_or_none(message['wal_config']),
                    quantization_config=json_or_none(message['quantization_config'])
                )
            )
        except Exception as exc:
            raise Exception(
                f'''
                Failed to create collection `{message["name"]}`
                '''
            ) from exc
    return pd.DataFrame(df)
