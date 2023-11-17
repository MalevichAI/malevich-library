from openai import AsyncOpenAI
from openai.types import ImagesResponse

from ..models.configuration.image import ImageConfiguration


async def exec_image(prompt: str, conf: ImageConfiguration) -> ImagesResponse:
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
