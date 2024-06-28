import json

import pandas as pd
from malevich.square import DF, Context, processor, scheme
from qdrant_client import QdrantClient

from .models import Index


@scheme()
class CreateIndexMessage:
    name: str
    field: str

@scheme()
class CreateIndexResponse:
    status: str

@processor()
def create_index(
    messages: DF[CreateIndexMessage],
    ctx: Context[Index]
) -> DF[CreateIndexResponse]:
    '''Create a collection in Qdrant.


    ## Input:

        A dataframe consisting of columns:

        - `name` (str): Name of the collection.
        - `field` (str): Name of the field.
        - `schema` (str): JSON string with the schema of the index


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

    -----

    Args:
        messages (DF[CreateIndexMessage]): A dataframe with names and parameters
        of the collections.
        ctx (Context[Qdrant]): context.

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
        raise Exception(f'Could not connect to `{client_url}`') from exc


    df = {
        'status': []
    }
    schema = ctx.app_cfg.schema
    for message in messages.to_dict(orient='records'):
        try:
            df['status'].append(
                str(
                    qdrant_client.create_payload_index(
                        collection_name=message['name'],
                        field_name=message['field'],
                        field_schema=schema
                    ).status
                )
            )
        except Exception as exc:
            raise Exception(
                f'''
                Creating index in `{message["name"]}` on field `{message["field"]}` failed!
                Try fixing the schema.
                '''  # noqa: E501
            ) from exc
    return pd.DataFrame(df)
