import json

import pandas as pd
from malevich.square import DF, Context, processor, scheme
from qdrant_client import QdrantClient

from .models import Update


@scheme()
class UploadIds:
    id: int | str | None

@scheme()
class UploadVectors:
    name: str
    vector: str

@scheme()
class UploadPayloads:
    payload: str

@scheme()
class UploadCollectionResponse:
    status: bool


@processor()
def upload_collection(
    ids: DF[UploadIds],
    vectors: DF[UploadVectors],
    payloads: DF[UploadPayloads],
    ctx: Context[Update]
) -> DF[UploadCollectionResponse]:
    '''
    Upload points in Qdrant.

    ## Input:

        Consists of three dataframes:
        `ids` (DF[UploadIds]): ids for each point.


    ## Output:

        A dataframe with column:
        - `status` (bool): Status of the operation. If True, collection was successfully created.


    ## Configuration:

        - `url`: str.
            URL location of your Qdrant DB.
        - `api_key`: str, default None.
            API key of your Qdrant DB.
        - `timeout`: int, default None.
            Connection timeout in seconds.
        - `https`: bool, default None.
            Whether HTTPS connection is used.
        - `use_vector_names`: bool, default True.
            Set to False to omit vector names. Only works if amount of vectors is equal to amount of payloads.
        - `use_ids`: bool, default True.
            Set to False to let Qdrant assign ids to payloads. Ignores the data in `ids` dataframe.


    ## Notes:

        IMPORTANT: Make sure that lenghts of dataframes are matched correctly.
        If `ids` and `payloads` have a length of <LENGTH>, then `vectors` should have a length of <NUM_VEC> * <LENGTH>, and each vector name should repeat exactly <LENGTH> times.

        ALSO IMPORTANT: Please set payloads for every point you add, empty JSON string works as well.

        If any element in `ids` is None, the dataframe will be ignored (same as `use_ids=False`).

    -----

    Args:
        messages (DF[UploadCollectionMessage]): A dataframe with names and parameters of the collections.
        ctx (Context[Update]): context.

    Returns:
        A dataframe of return statuses.
    ''' # noqa:E501

    def validate_vectors(length: int, use_names: bool = True) -> None:
        if use_names:
            lens = vectors.groupby(by=['name']).count()
            assert lens.nunique() == 1, "Vector names in the dataframe are mismatched!"
            assert lens.iloc[0, 0] == length, "Length of vectors does not match the length of payloads!" # noqa:E501
        else:
            assert len(vectors) == length, "`vectors` dataframe length mismatch!"

    def validate_ids(length: int, use_ids: bool = True) -> None:
        if use_ids:
            assert len(ids) == length, "`ids` dataframe length mismatch!"

    def join_by(series, delim=',') -> str:
        return delim.join(series)

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
    # If there are any ids that are None, we just omit them
    use_ids = ctx.app_cfg.use_ids and not ids.isna().any()
    use_vector_names = ctx.app_cfg.use_vector_names

    num_points = len(payloads)
    # Validate dimensions before transforming the data into a readable format
    validate_vectors(num_points, use_vector_names)
    validate_ids(num_points, use_ids)
    # Evil groupby magic, do not attempt at home
    # FIXME: probably not very efficient either, waiting for JSON to happen
    # Aggregate over the name,
    if use_vector_names:
        vec_grouped = vectors.groupby(
            by=['name']
        ).agg(
        # concatenate vector strings,
            lambda x: join_by(x, '|')
        # transform to dict over by index
        ).to_dict(orient='index')
        # Split and evaluate vector strings
        vec_grouped = {
            name : list(map(eval, value['vector'].split('|')))
            for name, value in vec_grouped.items()
        }
        # Reformat into subsequent vector items, suitable for `upload_collection()`
        vecs = [
            {
                name : vector[i]
                for name, vector in vec_grouped.items()
            }
            for i in range(num_points)
        ]
    else:
        vecs = list(map(eval, vectors['vector'].to_list()))
    # Transform payloads while we are at it
    try:
        qdrant_client.upload_collection(
            collection_name=collection_name,
            vectors=vecs,
            payload=list(map(json.loads, payloads['payload'].to_list())),
            ids=ids if use_ids else None,
            batch_size=batch_size,
            parallel=parallel
        )
    except Exception as exc:
        raise Exception(f'Upload to collection `{collection_name}` failed!') from exc # noqa:E501

    return pd.DataFrame(df)
