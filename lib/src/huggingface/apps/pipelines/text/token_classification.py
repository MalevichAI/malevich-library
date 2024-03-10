from collections import defaultdict
from typing import Optional

import pandas as pd
import pydantic
from malevich.square import DF, Context, processor, scheme
from transformers import TokenClassificationPipeline, pipeline

from .models import TokenClassification


@scheme()
class TokenClassificationInput:
    text: str


class TokenClassificationConfig(pydantic.BaseModel):
    model: Optional[str] = None
    tokenizer: Optional[str] = None
    device: Optional[str] = 'cpu'
    batch_size: Optional[int] = 1
    aggregation_strategy: Optional[str] = 'none'
    ignore_labels: Optional[str] = ["O"]
    keep_text: Optional[bool] = False
    keep_sentence_index: Optional[bool] = True


@processor()
def token_classification(
    text: DF[TokenClassificationInput], context: Context[TokenClassification]
    ):
    """Token classification using HuggingFace Transformers"

    The processor solves a problem of token classification using HuggingFace pipeline.

    ## Input:

        A dataframe with a column:
        - `text` (str): text to be classified.

    ## Output:

        A dataframe with columns:

        - `sentence_index` (str, optional): index of the sentence in the input dataframe
        - `entity` (str): entity name (according to the model)
        - `score` (float): confidence score
        - `index` (int): index of the token in the sentence
        - `word` (str): token text (according to the model)
        - `start` (int): start index of the token in the sentence (might be absent)
        - `end` (int): end index of the token in the sentence (might be absent)

    ## Configuration:

        - `ignore_labels`: list.
            List of labels to ignore (e.g. `["O"]`).
        - `keep_text`: bool.
            Whether to keep the input text in the output dataframe.
        - `keep_sentence_index`: bool.
            Whether to keep the sentence index in the output dataframe.
        - `model`: str.
            Model name (e.g. `dbmdz/bert-large-cased-finetuned-conll03-english`).
        - `tokenizer`: str.
            Tokenizer name (e.g. `bert-base-cased`).
        - `device`: str.
            Device to run the model on (`cpu` or `gpu`).
        - `batch_size`: int.
            Batch size to use for inference.
        - `aggregation_strategy`: str.
            Aggregation strategy to use for multiple entities per token.
            See [Aggregation strategy](https://huggingface.co/docs/transformers/v4.36.1/en/main_classes/pipelines#transformers.TokenClassificationPipeline.aggregation_strategy)

    -----

    Args:
        text (TokenClassificationInput): input dataframe with text to classify
        config (dict): configuration (see above)

    """  # noqa: E501
    data_ = text.text.to_list()
    try:
        ctx_ = TokenClassificationConfig(**context.app_cfg)
    except pydantic.ValidationError as e:
        errs_ = "\n".join(
            [f"{err_['loc'][0]}: {err_['msg']}"
             for err_ in e.errors()]
        )
        raise Exception(
            "Configuration is invalid. "
            "See errors below:\n" + errs_
        ) from e

    if ctx_.device == 'gpu' or ctx_.device == 'cuda':
        try:
            import torch
            if torch.cuda.is_available():
                ctx_.device = 0
                context.logger.warn(
                    "GPU is available. Switching to GPU mode."
                )
            else:
                ctx_.device = -1
        except ImportError:
            context.logger.warn(
                "PyTorch is not available. Switching to CPU mode."
            )
            ctx_.device = -1
    else:
        ctx_.device = -1

    pipeline_: TokenClassificationPipeline = pipeline(
        "ner",
        **ctx_.model_dump(
            exclude_none=True,
            exclude=["keep_text", "keep_sentence_index"]
        ),
    )

    results = pipeline_(data_)

    df_data = defaultdict(list)

    for text, (i, r) in zip(data_, enumerate(results)):
        if isinstance(r, dict):
            r = [r]

        for rec_ in r:
            df_data['sentence_index'].append(i)
            for k, v in rec_.items():
                df_data[k].append(v)

            if ctx_.keep_text:
                df_data['text'].append(text)

    context.logger.info(f"Stats: {k: len(v) for k,v in df_data.items()}")

    if not ctx_.keep_sentence_index:
        df_data.pop('sentence_index', None)

    return pd.DataFrame(df_data)
