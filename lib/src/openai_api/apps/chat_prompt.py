import asyncio
from typing import Any

import pandas as pd
from malevich.square import DF, Context, processor

from ..lib.chat import exec_chat
from .models import PromptCompletion


@processor()
async def prompt_completion(variables: DF[Any], ctx: Context[PromptCompletion]):
    """Use Chat Completions feature from OpenAI

    Chat completions enable you to chat with OpenAI
    using a prompt template

    Available models: https://platform.openai.com/docs/models

    To use the model you should set the following parameters:

    - `openai_api_key`: Your OpenAI API key. Get it here: https://platform.openai.com/api-keys
    - `user_prompt`: The prompt for the user

    Scroll down to see the full list of parameters.

    ## Input:

        A dataframe with variables to be used in the prompts. Each row of the
        dataframe will be used to generate a prompt. For example, if your prompt
        contains a name enclosed in {} like this:

        Hi! Write a story about {someone}

        You have to have a column `someone` in the input dataframe. For each
        of such variables you should have a separate column.

    ## Output:

        A dataframe with following columns:
            - content (str): the content of the model response

    ## Configuration:

        - `openai_api_key`: str.
            Your OpenAI API key.
        - `user_prompt`: str.
            The prompt for the user.
        - `system_prompt`: str.
            The prompt for the system.
        - `model`: str, default 'gpt-3.5-turbo'.
            The model to use.
        - `organization`: str, default None.
            The organization to use.
        - `max_retries`: int, default 3.
            The maximum number of retries.
        - `temperature`: float, default 0.9.
            The temperature.
        - `max_tokens`: int, default 150.
            The maximum number of tokens.
        - `top_p`: float, default 1.0.
            The top p.
        - `frequency_penalty`: float, default 0.0.
            The frequency penalty.
        - `presence_penalty`: float, default 0.0.
            The presence penalty.
        - `stop`: list, default [].
            The stop tokens.
        - `stream`: bool, default False.
            Whether to stream the response.
        - `n`: int, default 1.
            The number of completions to generate.
        - `response_format`: str, default None.
            The response format.

    ## Notes:
        If `response_format` is set to 'json_object', the system prompt should
        contain an instruction to return a JSON object, e.g.:

        ```
        You are a creative writer. You are writing a story about {names}.
        You should mention {colors} in your story.

        JSON:
        ```

        JSON completion only works with Davinci models

    -----

    Args:
        variables (DF[Any]): the variables to use in the prompts
        ctx (Context): the context

    Returns:
        DF[Any]: the chat messages
    """

    try:
        conf = ctx.app_cfg["conf"]
    except KeyError:
        raise Exception("OpenAI client not initialized.")

    assert "user_prompt" in ctx.app_cfg, "Missing `user_prompt` in app config."

    system_prompt = ctx.app_cfg.get("system_prompt", "")
    user_prompt = ctx.app_cfg["user_prompt"]

    messages = [
        [
            {"role": "system", "content": system_prompt.format(**_vars)},
            {"role": "user", "content": user_prompt.format(**_vars)},
        ]
        for _vars in variables.to_dict(orient="records")
    ]

    response = await asyncio.gather(*[exec_chat(x, conf) for x in messages])

    df = {
        "content": [],
    }

    for _response in response:
        for _message in _response:
            df["content"].append(_message.content)

    return pd.DataFrame(df)
