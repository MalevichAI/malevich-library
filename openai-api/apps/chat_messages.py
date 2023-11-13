import asyncio
from typing import Any

import pandas as pd
from malevich.square import DF, Context, processor, scheme
from openai import OpenAI
from pydantic import BaseModel

from ..lib.chat import exec_chat
from ..models.configuration import Configuration


@scheme()
class ChatMessages(BaseModel):
    index: int
    chat_index: int
    role: str
    content: str


@processor()
async def chat_with_openai_using_messages(inputs: DF[ChatMessages], ctx: Context):
    """Chat with OpenAI using fixed prompts and variables from a dataframe.

    Inputs:
        A dataframe with following columns:
            - index: the index of the row in the input dataframe
            - chat_index: the index of the message in the chat
            - role: the role of the message (either 'system' or 'user')
            - content: the content of the message

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
        - stop (list, default: []): the stop tokens
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
        client, conf = ctx.app_cfg["client"], ctx.app_cfg["conf"]
    except KeyError:
        raise Exception("OpenAI client not initialized.")

    messages = inputs.groupby("index")
    responses = []
    for i, message in messages:
        message_list = message.to_dict("records")
        message_list.sort(key=lambda x: x["chat_index"])

        responses.append(
            exec_chat(
                [{"role": x["role"], "content": x["content"]} for x in message_list],
                conf,
                client,
            )
        )

    answers = await asyncio.gather(*responses)
    outputs = []
    for i, message in messages:
        new_index = max(message["chat_index"]) + 1
        for j, answer in enumerate(answers[i]):
            message.loc[new_index + j] = {
                "index": i,
                "chat_index": new_index + j,
                "role": answer.role,
                "content": answer.content,
            }
        message.sort_values(by="chat_index", inplace=True)
        outputs.extend(message.to_dict("records"))

    return pd.DataFrame(outputs)
