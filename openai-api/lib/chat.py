from typing import List

from openai import OpenAI
from openai.types.chat import ChatCompletion, ChatCompletionMessage

from ..models.configuration import Configuration


async def exec_chat(
    messages: List[dict[str, str]],
    conf: Configuration,
    client: OpenAI = None
) -> List[ChatCompletionMessage]:
    if client is None:
        client = OpenAI(
            api_key=conf.api_key,
            max_retries=conf.max_retries,
            organization=conf.organization
        )

    response: ChatCompletion = client.chat.completions.create(
        messages=messages,
        model=conf.model,
        temperature=conf.temperature,
        max_tokens=conf.max_tokens,
        top_p=conf.top_p,
        frequency_penalty=conf.frequency_penalty,
        presence_penalty=conf.presence_penalty,
        stop=conf.stop,
        stream=conf.stream,
        n=conf.n,
        response_format={ "type": conf.response_format or "text" }
    )

    return [choice.message for choice in response.choices]
