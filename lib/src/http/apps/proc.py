import hashlib
import json
import os
from mimetypes import guess_extension

import aiohttp
import pandas as pd
from malevich.square import APP_DIR, DF, Context, processor

from .models import HttpRequest


def empty_string(string: str) -> bool:
    return string == ' ' or str(string) == 'nan'

def add_body(config, body: str|bytes, body_type, context: Context) -> dict:
    if body_type == 'json':
        config['json'] = json.loads(body)
    elif body_type == 'file':
        config['data'] = open(context.get_share_path(body), 'rb').read()
    elif body_type == 'text':
        config['data'] = body.encode()
    elif body_type == 'encoded':
        config['data'] = body
    return config

@processor()
async def http_request(df: DF, context: Context[HttpRequest]):
    """
    Make http requests.

    ## Input:

        A dataframe with columns:

        - `link` (str): URL to send request.
        - `body` (str, optional): Body for this request.
        - `body_type` (str, optional): Body type. One of the ['text', 'json', 'file', 'encoded']. If not specified or empty, will be taken from config.
        - `output_format` (str, optional): Output format. Either 'file' or 'text'. If not specified or empty, will be taken from config.

    ## Output:

        A dataframe with columns:

        - `link` (str): request URL.
        - `response` (str): response text, or filepath.

    ## Configuration:

        - `method`: str, default 'GET'.
            Request method.

        - `headers`: dict, default {}.
            Request headers.

        - `body_type`: str, default 'json'.
            Body content type. One of the ['text', 'json', 'file', 'encoded'].

        - `output_format`: str, default "text".
            Output format. For `text` returns the reponse in text format. For `file` will save result into a file and return filename.

    -----

    Args:
        df(DF): Dataframe with columns links, body(optional), body_types(optional) and output_format(optional)
    Returns:
        A dataframe with responses.
    """  # noqa: E501
    method = context.app_cfg.get("method", "GET")
    headers = context.app_cfg.get("headers", {})
    output = []
    for _, row in df.iterrows():
        async with aiohttp.ClientSession() as session:
            config = {'headers': headers}
            if 'body' in df.columns:
                body_type = (
                    row['body_type'] if 'body_type' in df.columns
                    and not empty_string(row['body_type'])
                    else context.app_cfg.get("body_type", 'json')
                )
                config = add_body(
                    config,
                    row['body'],
                    body_type,
                    context
                )
            response = await session.request(
                method, row['link'],
                **config
            )
            out = (
                row['output_format'] if 'output_format' in df.columns and
                not empty_string(row['output_format'])
                else context.app_cfg.get("output_format", 'text')
            )
            try:
                if out == 'file':
                    filename = (
                        f"{hashlib.sha256(row['link'].encode()).hexdigest()}"
                        f"{guess_extension(response.headers['content-type'].partition(';')[0].strip())}"
                    )
                    with open(os.path.join(APP_DIR, filename), 'wb') as f:
                        f.write(await response.read())
                    context.share(filename)
                    output.append([row['link'], filename])
                else:
                    output.append([row['link'], await response.text()])
            except Exception:
                output.append([row['link'], await response.text()])

    return pd.DataFrame(output, columns=['link', 'response'])
