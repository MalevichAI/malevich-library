import asyncio
from typing import AsyncGenerator, List

from langchain.chat_models import ChatOpenAI as LLMOpenAI
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from openai import AsyncOpenAI, OpenAI
from openai.types.beta.threads import TextContentBlock
from openai.types.chat import ChatCompletion, ChatCompletionMessage

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
        n=conf.n,
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



async def exec_assistant(
    message: dict[str, str], conf: Configuration
) -> str:
    client = AsyncOpenAI(
        api_key=conf.api_key,
        max_retries=conf.max_retries,
        organization=conf.organization,
    )
    assistant = await client.beta.assistants.create(
        model=message["model"],
        instructions=message["instructions"],
    )
    return assistant.id



async def exec_run(
    messages: List[dict[str, str]], conf: Configuration
) -> AsyncGenerator:
    client = OpenAI(
        api_key=conf.api_key,
        max_retries=conf.max_retries,
        organization=conf.organization
    )
    for message in messages:
        assistant = client.beta.assistants.retrieve(
            assistant_id=message["assistant_id"]
        )
        # if thread is NaN, create one
        if isinstance(message["thread_id"], float):
            run = client.beta.threads.create_and_run(
                assistant_id=message["assistant_id"],
                thread={
                    "messages": [
                        {
                            "role": message["role"],
                            "content": message["content"]
                        }
                    ]
                },
                model=assistant.model,
                temperature=conf.temperature,
                top_p=conf.top_p,
                max_completion_tokens=conf.max_tokens
            )
        else:
            # create a message, we do not need a handle for user messages
            client.beta.threads.messages.create(
                thread_id=message["thread_id"],
                role=message["role"],
                content=message["content"]
            )
            # create a run
            run = client.beta.threads.runs.create(
                thread_id=message["thread_id"],
                assistant_id=message["assistant_id"],
                model=assistant.model,
                temperature=conf.temperature,
                top_p=conf.top_p,
                max_completion_tokens=conf.max_tokens,
            )
        run_id = run.id
        thread_id = run.thread_id
        # poll until completed
        # no better way to do this until OpenAI updates the API
        max_iter, iter = 500, 0
        while run.status != "completed" and run.status != "failed" and iter <= max_iter:
            run = client.beta.threads.runs.retrieve(
                run_id=run_id,
                thread_id=thread_id
            )
            iter += 1
            await asyncio.sleep(0.1)
        # get the list of messages
        # latest messages are in the beginning of the list
        message_list = client.beta.threads.messages.list(
            thread_id=thread_id,
            limit=1
        )
        # message_list is always 1 element long, but we iterate just in case
        for msg in message_list.data:
            # messages consist of content blocks, e.g. text, image, audio
            # for now we only look for text
            # but it is possible to expand it in the future
            for content_block in msg.content:
                if isinstance(content_block, TextContentBlock):
                    yield (
                        content_block.text.value,
                        thread_id,
                        message["assistant_id"]
                    )


