from openai import AsyncOpenAI
from openai.types import ImagesResponse

from ..models.configuration.base import Configuration


async def exec_image(prompt: str, conf: Configuration) -> ImagesResponse:
    client = AsyncOpenAI(
        api_key=conf.api_key,
        max_retries=conf.max_retries,
        organization=conf.organization,
    )

    return await client.images.generate(
        prompt=prompt,
        model=conf.model,
        timeout=60,
    )
