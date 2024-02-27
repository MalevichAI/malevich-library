import pandas as pd
import pydantic
import torch
from malevich.square import DF, Context, processor, scheme
from transformers import pipeline


@scheme()
class TextInput:
    text: str
    """Text to classify"""


class TextClassificationConfig(pydantic.BaseModel):
    model: str = "distilbert-base-uncased-finetuned-sst-2-english"
    """Name of the model to use in the pipeline"""

    top_k: int = 1
    """Number of top labels to return"""

    functions_to_apply: str = "default"
    """ The function to apply to the model outputs in order to retrieve the scores.
    Accepts four different values:

    If this argument is not specified, then it will apply the
    following functions according to the number of labels:

    - If the model has a single label, will apply the sigmoid function on the output.
    - If the model has several labels, will apply the softmax function on the output.

    Possible values are:

    "sigmoid": Applies the sigmoid function on the output.
    "softmax": Applies the softmax function on the output.
    "none": Does not apply any function on the output.
    """


@processor()
def classify_text(text: DF[TextInput], context: Context):
    """
    Classify text with HuggingFace Transformers.

    ## Input:

        A dataframe with columns:

        - `text` (string): The text to classify

    ## Output:

        Number of rows is exactly number of input rows times `top_k` parameter.
        It is a dataframe with columns:

            - text (string): The text used for classification
            - label (str): The label associated to the text
            - score (float): The probability associated to the label

    ## Configuration:

        - `model`: string. default "distilbert-base-uncased-finetuned-sst-2-english".
            Name of the model to use in the pipeline
        - `top_k`: int. default 1.
            Number of top labels to return
        - `functions_to_apply`: string. default "default".
            The function to apply to the model outputs in order to retrieve the scores.
            Accepts four different values:
            - `"default"`: If this argument is not specified, then it will apply the
                following functions according to the number of labels:
                - If the model has a single label, will apply the sigmoid function on the output.
                - If the model has several labels, will apply the softmax function on the output.
            - `"sigmoid"`: Applies the sigmoid function on the output.
            - `"softmax"`: Applies the softmax function on the output.
            - `"none"`: Does not apply any function to the output.

    -----

    Args:

        text: A collection of texts to classify
        config: Configuration (see above)

    Returns:
        Collection with labels, scores and the original texts
    """  # noqa: E501
    try:
        config = TextClassificationConfig(**context.app_cfg)
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
            task='text-classification',
            device='cuda' if torch.cuda.is_available() else 'cpu',
        )
    except Exception:
        context.logger.error(
            "Got an error while trying to create the pipeline. "
            f"Probably the model name `{config.model }`is incorrect "
            "or does not support text classification."
        )
        raise

    responses: list[dict] = p(text.text.to_list())
    if not isinstance(responses, list):
        # If the pipeline returns a single conversation,
        # we need to wrap it into a list
        responses = [responses]

    output_records = []
    for r, text in zip(responses, text.text):
        if isinstance(r, dict):
            output_records.append({
                **r,
                "text": text
            })
        else:
            for rec in r:
                output_records.append({
                    **rec,
                    "text": text
                })

    return pd.DataFrame(output_records)