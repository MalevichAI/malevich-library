import pandas as pd
import torch
from malevich.square import DF, Context, processor, scheme
from transformers import pipeline

from .models import SummarizeText


@scheme()
class TextInput:
    text: str
    """Text to classify"""

@processor()
def summarize_text(text: DF[TextInput], context: Context[SummarizeText]):
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

        - `model`: str, default 'none'.
            Name of the model to use in the pipeline.

    -----

    Args:

        text: A collection of texts to summarize
        config: Configuration (see above)

    Returns:
        Collection with summaries and the original texts
    """  # noqa: E501

    try:
        p = pipeline(
            model=context.app_cfg.model,
            task='summarization',
            device='cuda' if torch.cuda.is_available() else 'cpu',
        )
    except Exception:
        context.logger.error(
            "Got an error while trying to create the pipeline. "
            f"Probably the model name `{context.app_cfg.model }`is incorrect "
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
