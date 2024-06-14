import pandas as pd
from malevich.square import DF, Context, processor
from qdrant_client import QdrantClient

from .models import Qdrant


@processor()
def get_collections(
    ctx: Context[Qdrant]
) -> DF:
    '''Create a collection in Qdrant.

    ## Input:

        A dataframe consisting of columns:
        - `name` (str): name of the collection.
        - `vector_size` (dict[str, int]): names and sizes of vectors in the collection.
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
        'collections': []
    }
    for collection in qdrant_client.get_collections().collections:
        df['collections'].append(collection.name)

    return pd.DataFrame(df)
