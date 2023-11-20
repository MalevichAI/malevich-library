from typing import List

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion, ChatCompletionMessage

from langchain.chat_models import ChatOpenAI as LLMOpenAI
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate

from ..models.configuration.base import Configuration


async def exec_chat(
    messages: List[dict[str, str]], conf: Configuration
) -> List[ChatCompletionMessage]:
    client = AsyncOpenAI(
        api_key=conf.api_key,
        max_retries=conf.max_retries,
        organization=conf.organization,
    )

    response: ChatCompletion = await client.chat.completions.create(
        messages=messages,
        model=conf.model or 'gpt-3.5-turbo',
        temperature=conf.temperature,
        max_tokens=conf.max_tokens,
        top_p=conf.top_p,
        frequency_penalty=conf.frequency_penalty,
        presence_penalty=conf.presence_penalty,
        stop=conf.stop,
        stream=conf.stream,
        n=conf.n,
        response_format={"type": conf.response_format or "text"},
    )

    return [choice.message for choice in response.choices]


async def exec_structured_chat(
    message: str, conf: Configuration, schemas: List[ResponseSchema]
) -> List[dict[str, str]]:
    client = LLMOpenAI(
        model=conf.model or 'gpt-3.5-turbo',
        api_key=conf.api_key,
        max_retries=conf.max_retries,
        temperature=conf.temperature,
        max_tokens=conf.max_tokens,
        top_p=conf.top_p,
        frequency_penalty=conf.frequency_penalty,
        presence_penalty=conf.presence_penalty,
        n=conf.n,
    )

    # print(schemas)
    output_parser = StructuredOutputParser.from_response_schemas(schemas)

    prompt = ChatPromptTemplate(
        messages=[
            HumanMessagePromptTemplate.from_template(
                message + "\n{format_instructions}",
            )
            # for message in messages if message
        ],
        partial_variables={
            "format_instructions": output_parser.get_format_instructions()
        },
    )


    output = await client.ainvoke(
        prompt.format_prompt().to_messages()
    )

    return output_parser.parse(output.content.replace('\n', ''))
