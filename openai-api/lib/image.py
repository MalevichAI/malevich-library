from openai import OpenAI

from ..models.configuration.image import ImageConfiguration


def exec_image(
    prompt: str,
    conf: ImageConfiguration
):
    client = OpenAI(
        api_key=conf.api_key,
        max_retries=conf.max_retries,
        organization=conf.organization
    )

    try:
        return client.images.generate(
            prompt=prompt,
            model=conf.model,
            #quality=conf.quality,
            #style=conf.style,
            timeout=60
        ).data[0].url
    except Exception as e:
        return str(e)
