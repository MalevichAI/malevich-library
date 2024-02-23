import pandas as pd
import pydantic
import torch
from malevich.square import DF, Context, processor, scheme
from transformers import pipeline


@scheme()
class TextInput:
    text: str
    """Text to classify"""


class TextSummarizationConfig(pydantic.BaseModel):
    model: str | None= None
    """Name of the model to use in the pipeline"""



@processor()
def summarize_text(text: DF[TextInput], context: Context):
    """
    Summarize text with HuggingFace Transformers.

    ## Input:

        A dataframe with columns:

        - `text` (string): The text to classify

    ## Output:

        It is a dataframe with columns:

            - text (string): The text used for summarization
            - summary (str): The summary of the text

    ## Configuration:

        - `model`: string. default is default summary model at HF.
            Name of the model to use in the pipeline

    -----

    Args:

        text: A collection of texts to summarize
        config: Configuration (see above)

    Returns:
        Collection with summaries and the original texts
    """  # noqa: E501
    try:
        config = TextSummarizationConfig(**context.app_cfg)
    except pydantic.ValidationError as err:
        context.logger.error(
            "Got an error while trying to get the config. "
            '. '.join([
                f"Field `{err['loc'][0]}` is not correct: {err['msg']}"
                for err in err.errors()
            ])
        )
        raise
    try:
        p = pipeline(
            model=config.model,
            task='summarization',
            device='cuda' if torch.cuda.is_available() else 'cpu',
        )
    except Exception:
        context.logger.error(
            "Got an error while trying to create the pipeline. "
            f"Probably the model name `{config.model }`is incorrect "
            "or does not support text summarization."
        )
        raise

    responses: list[dict] = p(text.text.to_list())
    if not isinstance(responses, list):
        # If the pipeline returns a single conversation,
        # we need to wrap it into a list
        responses = [responses]

    assert len(text.text) == len(responses), \
        "Number of responses should match number of inputs"

    return pd.DataFrame(
        [{"text": text, "summary": summary['summary_text']}
         for text, summary in zip(text.text, responses)]
    )
