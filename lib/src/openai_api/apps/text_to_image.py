import asyncio
from typing import Any

import pandas as pd
from malevich.square import DF, Context, processor

from ..lib.image import exec_image


@processor()
async def text_to_image(
    variables: DF[Any],
    ctx: Context
):
    """Use Text to Image feature from OpenAI

    Text to Image enables you to generate images from text prompts.
    To use this processor you should set the following parameters:

    - `openai_api_key`: Your OpenAI API key. Get it here: https://platform.openai.com/api-keys
    - `user_prompt`: The prompt for the user

    Inputs:

        A dataframe with variables to be used in the prompts. Each row of the
        dataframe will be used to generate a prompt. For example, if your prompt
        contains a name enclosed in {} like this:

        Hi! Write a story about {someone}

        You have to have a column `someone` in the input dataframe. For each
        of such variables you should have a separate column.

    Outputs:

        A dataframe with following column:
        - links (str): links to images

    Configuration:

        - openai_api_key (str, required): your OpenAI API key
        - user_prompt (str, required): the prompt for the user
        - model (str, default: 'dall-e-3'): the model to use

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
        'link': [x.data[0].url for x in outputs]
    })


