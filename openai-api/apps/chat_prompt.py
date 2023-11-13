import asyncio
from typing import Any

import pandas as pd
from malevich.square import DF, Context, processor
from openai import OpenAI

from ..lib.chat import exec_chat
from ..models.configuration import Configuration


@processor()
async def chat_with_openai_using_prompts(
    variables: DF[Any],
    ctx:  Context
):
    """Chat with OpenAI using fixed prompts and variables from a dataframe.

    Inputs:
        A dataframe with variables to be used in the prompts. Each row of the
        dataframe will be used to generate a prompt.

    Outputs:
        A dataframe with the following columns:
        - index: the index of the row in the input dataframe
        - chat_index: the index of the message in the chat
        - role: the role of the message (either 'system' or 'user')
        - content: the content of the message

    Configuration:

        - openai_api_key (str, required): your OpenAI API key
        - system_prompt (str, required): the prompt for the system
        - user_prompt (str, required): the prompt for the user
        - model (str, default: 'gpt-3.5-turbo'): the model to use
        - organization (str, default: None): the organization to use
        - max_retries (int, default: 3): the maximum number of retries
        - temperature (float, default: 0.9): the temperature
        - max_tokens (int, default: 150): the maximum number of tokens
        - top_p (float, default: 1.0): the top p
        - frequency_penalty (float, default: 0.0): the frequency penalty
        - presence_penalty (float, default: 0.0): the presence penalty
        - stop (list, default: []]): the stop tokens
        - stream (bool, default: False): whether to stream the response
        - n (int, default: 1): the number of completions to generate
        - response_format (str, default: None): the response format
        - output_history (bool, default: False): whether to output the history

    Notes:
        If `response_format` is set to 'json_object', the system prompt should
        contain an instruction to return a JSON object, e.g.:

        ```
        You are a creative writer. You are writing a story about {names}.
        You should mention {colors} in your story.

        JSON:
        ```

        JSON completion only works with Davinci models

    Args:
        variables (DF[Any]): the variables to use in the prompts
        ctx (Context): the context

    Returns:
        DF[Any]: the chat messages
    """

    try:
        client, conf = ctx.app_cfg['client'], ctx.app_cfg['conf']
    except KeyError:
        raise Exception(
           "OpenAI client not initialized."
        )

    assert 'system_prompt' in ctx.app_cfg, \
        "Missing `system_prompt` in app config."

    assert 'user_prompt' in ctx.app_cfg, \
        "Missing `user_prompt` in app config."

    system_prompt = ctx.app_cfg['system_prompt']
    user_prompt = ctx.app_cfg['user_prompt']

    messages = [
        [{
            "role": "system",
            "content": system_prompt.format(**_vars)
        },
        {
            "role": "user",
            "content": user_prompt.format(**_vars)
         }] for _vars in variables.to_dict(orient='records')
    ]

    response = await asyncio.gather(
        *map(lambda x: exec_chat(x, conf, client),
            messages
        )
    )

    df = {
        'index': [],
        'chat_index': [],
        'role': [],
        'content': [],
    }

    if conf.output_history:
        for i, message in enumerate(messages):
            for j, _message in enumerate(message, start=1):
                df['index'].append(variables.index[i])
                df['chat_index'].append(j)
                df['role'].append(_message['role'])
                df['content'].append(_message['content'])

    for i, _response in enumerate(response):
        for _message in _response:
            df['index'].append(variables.index[i])
            df['chat_index'].append(3)
            df['role'].append(_message.role)
            df['content'].append(_message.content)

    return pd.DataFrame(
        df
    )
