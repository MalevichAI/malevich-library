from concurrent.futures import ProcessPoolExecutor
from typing import Any
import asyncio
import pandas as pd
from malevich.square import DF, Context, processor

from ..lib.image import exec_image


@processor()
async def text_to_image(
    variables: DF[Any],
    ctx: Context
):
    """Converts image to text using OpenAI API

    Inputs:

        A dataframe with variables to be used in the prompts. Each row of the
        dataframe will be used to generate a prompt.

    Outputs:

        A dataframe with following column:
        - index (int): the index of the variable
        - content (str): the content of the model response

    Configuration:

        - openai_api_key (str, required): your OpenAI API key
        - model (str, default: 'dall-e-3'): the model to use
        - user_prompt (str, required): the prompt for the user

    Args:
        variables (DF[ImageLinks]): Dataframe with variables
            for the prompt
        ctx (Context): Context object

    Returns:
        Dataframe with links to images
    """

    try:
        conf = ctx.app_cfg['conf']
    except KeyError:
        raise Exception(
           "OpenAI client not initialized."
        )

    user_prompt = ctx.app_cfg.get('user_prompt')

    inputs = [
        user_prompt.format(**__vars)
        for __vars in variables.to_dict(orient='records')
    ]

    outputs = await asyncio.gather(
        *[exec_image(x, conf) for x in inputs],
    )

    return pd.DataFrame({
        'links': [x.data[0].url for x in outputs]
    })


