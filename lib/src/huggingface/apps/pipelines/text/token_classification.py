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

        - `ignore_labels`: list, default ["0"].
            List of labels to ignore (e.g. `["O"]`).
        - `keep_text`: bool, default False.
            Whether to keep the input text in the output dataframe.
        - `keep_sentence_index`: bool, default True.
            Whether to keep the sentence index in the output dataframe.
        - `model`: str, default None.
            Model name (e.g. `dbmdz/bert-large-cased-finetuned-conll03-english`).
        - `tokenizer`: str, default None.
            Tokenizer name (e.g. `bert-base-cased`).
        - `device`: str, default 'cpu'.
            Device to run the model on (`cpu` or `gpu`).
        - `batch_size`: int, default 1.
            Batch size to use for inference.
        - `aggregation_strategy`: str, default 'none'.
            Aggregation strategy to use for multiple entities per token.
            See [Aggregation strategy](https://huggingface.co/docs/transformers/v4.36.1/en/main_classes/pipelines#transformers.TokenClassificationPipeline.aggregation_strategy)

    -----

    Args:
        text (TokenClassificationInput): input dataframe with text to classify
        config (dict): configuration (see above)

    """  # noqa: E501
    data_ = text.text.to_list()

    if context.app_cfg.device == 'gpu' or context.app_cfg.device == 'cuda':
        try:
            import torch
            if torch.cuda.is_available():
                context.app_cfg.device = 0
                context.logger.warn(
                    "GPU is available. Switching to GPU mode."
                )
            else:
                context.app_cfg.device = -1
        except ImportError:
            context.logger.warn(
                "PyTorch is not available. Switching to CPU mode."
            )
            context.app_cfg.device = -1
    else:
        context.app_cfg.device = -1

    pipeline_: TokenClassificationPipeline = pipeline(
        "ner",
        **context.app_cfg.model_dump(
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

            if context.app_cfg.keep_text:
                df_data['text'].append(text)

    context.logger.info(f"Stats: {k: len(v) for k,v in df_data.items()}")

    if not context.app_cfg.keep_sentence_index:
        df_data.pop('sentence_index', None)

    return pd.DataFrame(df_data)
