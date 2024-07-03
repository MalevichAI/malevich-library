import asyncio

import pandas as pd
from malevich.square import DF, Context, processor, scheme

from ..lib.chat import exec_assistant
from .models import CreateAssistant


@scheme()
class CreateAssistantMessage:
    name: str
    instructions: str
    model: str


@processor()
async def create_assistant(
    initials: DF[CreateAssistantMessage],
    ctx: Context[CreateAssistant]
):
    """Create an assistant with OpenAI Chat Assistant feature.

    ## Input:

        A dataframe with columns:
        - `name` (str): name of the assistant
        - `instructions` (str): initial instructions for the assistant
        - `model` (str): model used for assistant

    ## Output:

        A dataframe with column:
        - `assistant_id` (str): id of the assistant

    ## Configuration:

        - `openai_api_key`: str.
            Your OpenAI API key.
        - `model`: str, default 'gpt-3.5-turbo'.
            Default model to use. Overriden by `model` column in the input.
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

    -----

    Args:
        initials (DF[CreateAssistantMessage]): initial settings of the assistant
        ctx (Context): the context

    Returns:
        DF[Any]: the ids of the assistants
    """
    try:
        conf = ctx.app_cfg["conf"]
    except KeyError:
        raise Exception("OpenAI client not initialized.")

    messages = [
        {
            "name": _vars.get("name", ""),
            "instructions": _vars.get("instructions", ""),
            "model": conf.model if _vars.get("model", "") == "" else _vars["model"],
        } for _vars in initials.to_dict(orient="records")
    ]

    response = await asyncio.gather(*[exec_assistant(x, conf) for x in messages])

    df = {
        "assistant_id": []
    }

    for _response in response:
        df["assistant_id"].append(_response)

    return pd.DataFrame(df)
