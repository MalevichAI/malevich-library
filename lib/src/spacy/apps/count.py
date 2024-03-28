from collections import Counter

import pandas as pd
from malevich.square import DF, Context, processor, scheme
from pydantic import BaseModel

from .models import CountWordPercentage


@scheme()
class TextKey(BaseModel):
    idx: str|int
    text: str
    keywords: str

@processor()
def count_word_percentage(df: DF[TextKey], context: Context[CountWordPercentage]):
    """
    Count keyword frequency in text.

    ## Input:

        A dataframe with columns:

        - idx (str): Row id.
        - text (str): Text to analyze.
        - keywords (str): Keywords, separated by delimeter, which is set in configuration.

    ## Output:

        A dataframe with columns:

        - idx (str): Row id.
        - key (str): Key name.
        - frequency (str): Key frequency in the text.

    ## Configuration:

        - language: str, default 'en'.
            Text language.
        - delimeter: str, default ','.
            Keywords separator.
        - metric_unit: str, default 'float'.
            Output metric unit. Either "percent" or "float".

    -----
    Args:
        df(DF[TextKey]): A dataframe with text and keywords.
    Retuns:
        A dataframe with metric values
    """  # noqa: E501
    model = context.common.model
    delim = context.app_cfg.get("delimeter", ",")
    metric = context.app_cfg.get("metric_unit", "float")
    outputs = []
    for _, row in df.iterrows():
        keywords = row["keywords"].split(delim)
        tokens = model(row["text"])
        tokens = [
            x.lemma_.strip() for x in tokens if x.lemma_ not in "!-;:\"\'_/\\—,.?"
        ]
        mappd = Counter(tokens)
        res = {key: val / sum(mappd.values()) for key, val in mappd.items()}
        key_percentage = []
        for key in keywords:
            lemma = model(key.strip())[0].lemma_
            key_percentage.append({"key": key, "percentage": res.get(lemma, 0)})

        for x in key_percentage:
            if metric == 'percent':
                string = f"{x['percentage'] * 100}%"
            else:
                string = x['percentage']

            outputs.append(
                [
                    row["idx"],
                    x['key'],
                    string
                ]
            )
    return pd.DataFrame(outputs, columns=['idx','key', 'frequency'])
