import json

import pandas as pd
from malevich.square import DF, Context, processor, scheme
from pydantic import BaseModel

from .types import SpaCy


@scheme()
class Text(BaseModel):
    text: str


@processor()
def extract_named_entities(
    df: DF,
    context: Context,
):
    """Extracts named entities from text.

    Input:
        A dataframe with a column named `text` containing text.

    Output:
        The format of dataframe depends on the configuration provided.

        If `output_format` is `list`, the output will be a dataframe
        with a column named `entities` containing a list of named entities without
        tag specifications.

        If `output_format` is `struct`, the output will be a dataframe
        with a column named `entities` containing a JSON object with the following
        structure:
        ```
        {
            "text": "text",
            "start_char": 0,
            "end_char": 4,
            "label": "PERSON"
        }
        ```
        The `label` is the tag specification of the named entity.

        If `output_format` is `table`, the output will be a dataframe with the following
        columns:
        - `text`: The text of the named entity.
        - `start_char`: The starting character of the named entity.
        - `end_char`: The ending character of the named entity.
        - `label`: The tag specification of the named entity.

    Configuration:

        - output_format: str, default "list".
            The format of the output. Valid values are "list", "struct", and "table".
        - model_name: str, default "en_core_web_sm".
            The name of the model to use. See https://spacy.io/models for available models.
        - filter_labels: list[str], default None.
            A list of labels to filter the named entities by. If None, all named entities will be returned.


    Args:
        df (DF):
            A dataframe with a column named `text` containing text.

    Returns:
        A dataframe with a column named `entities` containing a list of named entities without
        tag specifications.
    """  # noqa: E501
    backend: SpaCy = context.common
    filter_labels = context.app_cfg.get("filter_labels", None)
    output_format = context.app_cfg.get("output_format", "list")

    outputs = []
    for _, row in df.iterrows():
        doc = backend.model(row["text"])
        entities = [
            {
                "text": ent.text,
                "start_char": ent.start_char,
                "end_char": ent.end_char,
                "label": ent.label_,
            }
            for ent in doc.ents
            if filter_labels is None or ent.label_ in filter_labels
        ]
        if output_format == "list":
            outputs.append(' '.join([ent["text"] for ent in entities]))
        elif output_format == "struct":
            outputs.append(json.dumps(entities))
        elif output_format == "table":
            outputs.extend(entities)
        else:
            raise ValueError(f"Invalid output format: {output_format}")

    if output_format == "list":
        return pd.DataFrame({"entities": outputs})
    elif output_format == "struct":
        return pd.DataFrame({"entities": outputs})
    elif output_format == "table":
        return pd.DataFrame(outputs)
    else:
        raise ValueError(f"Invalid output format: {output_format}")

