from typing import Any
import asyncio
import pandas as pd
from malevich.square import DF, Context, processor, scheme

from ..lib.chat import exec_run
from .models import ThreadPromptCompletion

@scheme()
class ThreadInputMessage:
    message: str
    thread_id: str

@processor()
async def thread_completion(variables: DF[ThreadInputMessage], ctx: Context[ThreadPromptCompletion]):
    '''Use Chat Assistant feature from OpenAI with multiple threads.

    Input:
    
    Output:

    Configuration:

    -----
    '''
    try:
        conf = ctx.app_cfg["conf"]
    except KeyError:
        raise Exception("OpenAI client not initialized.")
        
    system_prompt = ctx.app_cfg.get("system_prompt", "")
    assistant_id = ctx.app_cfg.get("assistant_id")


    messages = [
        {
            "role": "user", 
            "content": _vars["message"], 
            "thread_id": _vars["thread_id"], 
            "assistant_id": assistant_id
        }
        for _vars in variables.to_dict(orient="records")
    ]

    response = [item async for item in exec_run(messages, conf)]

    df = {
        "content": [],
        "thread_id": []
    }

    for message, thread_id in response:
        df["content"].append(message)
        df["thread_id"].append(thread_id)

    return pd.DataFrame(df)