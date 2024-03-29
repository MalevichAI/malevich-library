import asyncio
import os
import shutil
from typing import Any

import pandas as pd
from malevich.square import APP_DIR, DF, Context, processor

from ..lib.tts import exec_tts
from .models import TextToSpeech


@processor()
async def text_to_speech(variables: DF[Any], ctx: Context[TextToSpeech]):
    """Use Text-to-Speech feature from OpenAI

    Produce quality audio from text using OpenAI API

    To use the model you should set the following parameters:

    - `openai_api_key`: Your OpenAI API key. Get it here: https://platform.openai.com/api-keys

    Scroll down to see the full list of parameters.

    ## Input:

        A dataframe with a column:
        - `text` (str): the text to be converted to speech

    ## Output:

        A dataframe with a column:
            - `filename` (str): a key of shared .mp3 files for each input

    ## Configuration:

        - `openai_api_key`: str.
            Your OpenAI API key.
        - `model`: str, default 'tts-1'.
            The model to use.
        - `voice`: str, default 'alloy'.
            The voice to use. One of 'alloy', 'echo', 'fable', 'onyx', 'nova', and 'shimmer'.

    -----

    Args:
        variables (DF[Any]): the variables to use in the prompts
        ctx (Context): the context

    Returns:
        DF[Any]: the chat messages
    """  # noqa: E501

    try:
        conf = ctx.app_cfg["conf"]
    except KeyError:
        raise Exception("OpenAI client not initialized.")

    files = [f"voice_{i}_{ctx.run_id}.mp3" for i in range(len(variables))]

    await asyncio.gather(*[exec_tts(x, conf, f) for x, f in zip(
        variables.text.to_list(),
        files
    )])

    for f in files:
        shutil.move(f, os.path.join(APP_DIR, f))
        ctx.share(f)
        ctx.synchronize([f])

    return pd.DataFrame({"filename": files})
