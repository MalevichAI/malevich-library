from openai import AsyncOpenAI
from openai.types import ImagesResponse

from ..models.configuration.image import ImageConfiguration


async def exec_image(prompt: str, conf: ImageConfiguration) -> ImagesResponse:
    client = AsyncOpenAI(
        api_key=conf.api_key,
        max_retries=conf.max_retries,
        organization=conf.organization,
    )

    return await client.audio.speech.create(
        prompt=prompt,
        model=conf.model,
        # quality=conf.quality,
        # style=conf.style,
        timeout=60,
    )
