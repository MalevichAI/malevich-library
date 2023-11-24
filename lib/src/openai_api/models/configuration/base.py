from typing import Optional

from pydantic import BaseModel, Field


class Configuration(BaseModel):
    api_key: str = Field(
        ...,
        description="Your OpenAI API key. Get it here: https://platform.openai.com/api-keys",
    )

    mode: Optional[str] = Field(
        None,
        description="The mode to use. Available modes: `image`, `text`. Automatically detected if not set",  # noqa: E501
    )

    model: Optional[str] = Field(
        None,
        description="The model to use. Available models: https://platform.openai.com/docs/models",
    )

    organization: Optional[str] = Field(
        None,
        description="The organization on Open AI Platform to use",
    )

    max_retries: int = Field(
        3,
        description="The maximum number of retries in case of API failure",
    )

    include_index: bool = Field(
        False,
        description="Whether to include the index of rows in the response.",
    )

    quality: Optional[str] = Field(
        "standard",
        description="The quality of the response. Default is 'standard'.",
    )

    size: Optional[str] = Field(
        None,
        description="The size of the response. Optional field.",
    )

    style: Optional[str] = Field(
        None,
        description="The style of the response. Optional field.",
    )

    temperature: Optional[float] = Field(
        0.9,
        description="The temperature of the response. Default is 0.9.",
    )

    max_tokens: Optional[int] = Field(
        2048,
        description="The maximum number of tokens in the response. Default is 2048.",
    )

    top_p: float = Field(
        1.0,
        description="The top-p value for nucleus sampling. Default is 1.0.",
    )

    frequency_penalty: float = Field(
        0.0,
        description="The frequency penalty for nucleus sampling. Default is 0.0.",
    )

    presence_penalty: float = Field(
        0.0,
        description="The presence penalty for nucleus sampling. Default is 0.0.",
    )

    stop: list[str] = Field(
        [],
        description="The list of stop words. Default is an empty list.",
    )

    n: int = Field(
        1,
        description="The number of completions to generate. Default is 1.",
    )

    best_of: int = Field(
        1,
        description="The number of best completions to return. Default is 1.",
    )
