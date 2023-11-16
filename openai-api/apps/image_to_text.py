from concurrent.futures import ProcessPoolExecutor
from typing import Any

import pandas as pd
from malevich.square import DF, Context, processor

from ..lib.image import exec_image


@processor()
def image_to_text(
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
        - user_prompt (str, required): the prompt for the user
        - quality (str, default: 'standard'): the quality of the image
        - size (str, default: '512x512'): the size of the image
        - style (str, default: 'natural'): the style of the image

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

    # with ProcessPoolExecutor() as executor:
    #     outputs = executor.map(
    #         exec_image,
    #         inputs,
    #         [conf] * len(inputs)
    #     )

    outputs = [
        await exec_image(x, conf)
        for x in inputs
    ]

    return pd.DataFrame({
        'links': outputs
    })


