import numpy as np
import pandas as pd
import torch
from malevich.square import DF, Context, processor, scheme

from sentence_transformers import SentenceTransformer

from .models import Embedding


@scheme()
class CreateEmbeddingMessage:
    text: str

@processor()
def create_embeddings(
    texts: DF[CreateEmbeddingMessage],
    ctx: Context[Embedding]
):
    """Create an assistant with OpenAI Chat Assistant feature.

    ## Input:

        A dataframe with columns:
        - `text` (str): text to embed

    ## Output:

        A dataframe with column:
        - `embedding` (str): string reprentation of generated embeddings

    ## Configuration:

        - `device`: str, default 'cpu'.
            Device to run generation on.
        - `model`: str, default 'all-MiniLM-L6-v2'.
            Transformer model to use.
        - `mode`: str, default 'sentence_embedding'.
            Type of embedding. Values: 'sentence_embedding', 'token_embedding'.

    -----

    Args:
        texts (DF[CreateEmbeddingMessage]): initial settings of the assistant
        ctx (Context): the context

    Returns:
        DF[Any]: the string representations of embeddings
    """
    device: str = ctx.app_cfg.device if (
        torch.cuda.is_available() and ctx.app_cfg.device == 'cuda'
    ) else 'cpu'
    model: str = ctx.app_cfg.model
    mode: str = ctx.app_cfg.mode
    batch_size: int = ctx.app_cfg.batch_size

    df = {
        "embedding": []
    }

    transformer = SentenceTransformer(
        model_name_or_path=model,
        device=device
    )

    inputs: list[str] = [var['text'] for var in texts.to_dict(orient='records')]
    try:
        embeds: list[np.ndarray] = transformer.encode(
            sentences=inputs,
            output_value=mode,
            batch_size=batch_size
        )
    except Exception as exc:
        print(exc)
        embeds = []

    for _response in embeds:
        df["embedding"].append(repr(_response.tolist()))

    return pd.DataFrame(df)
