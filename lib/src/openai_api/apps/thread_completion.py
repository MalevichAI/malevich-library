import pandas as pd
from malevich.square import DF, Context, processor, scheme

from ..lib.chat import exec_run
from .models import ThreadCompletion


@scheme()
class ThreadInputMessage:
    message: str
    thread_id: str
    assistant_id: str


@processor()
async def thread_completion(
    messages: DF[ThreadInputMessage],
    ctx: Context[ThreadCompletion]
):
    """Use Chat Assistant feature from OpenAI with multiple threads.

    Thread completions allow you to interact with assistants in different threads.

    Available models: https://platform.openai.com/docs/models

    To use the model you should set the following parameters:

    - `openai_api_key`: Your OpenAI API key. Get it here: https://platform.openai.com/api-keys

    Scroll down to see the full list of parameters.

    ## Input:

        A dataframe with columns:
        - `message` (str): text message to the assistant
        - `thread_id` (str): id of the thread the message is designated to
        - `assistant_id` (str): id of the assistant the message is designated to

    ## Output:

        A dataframe with columns:
        - `message` (str): text of the response from the assistant
        - `thread_id` (str): id of the thread the message arrived from
        - `assistant_id` (str): id of the assistant the message arrived from

    ## Configuration:

        - `openai_api_key`: str.
            Your OpenAI API key.
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

    -----

    Args:
        messages (DF[ThreadInputMessage]): messages for assistants used in the prompt
        cts (Context): the context

    Returns:
        DF[Any]: the responses from the assistants in designated threads
    """
    try:
        conf = ctx.app_cfg["conf"]
    except KeyError:
        raise Exception("OpenAI client not initialized.")

    # system_prompt = ctx.app_cfg.get("system_prompt", "")
    # assistant_id = ctx.app_cfg.get("assistant_id")


    messages = [
        {
            "role": "user",
            "content": _vars["message"],
            "thread_id": _vars["thread_id"],
            "assistant_id": _vars["assistant_id"]
        }
        for _vars in messages.to_dict(orient="records")
    ]

    response = [item async for item in exec_run(messages, conf)]

    df = {
        "content": [],
        "thread_id": [],
        "assistant_id": []
    }

    for message, thread_id, assistant_id in response:
        df["content"].append(message)
        df["thread_id"].append(thread_id)
        df["assistant_id"].append(assistant_id)

    return pd.DataFrame(df)
