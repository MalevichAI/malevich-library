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
        for i in range(len(keywords)):
            tokens = model(keywords[i].strip())
            keywords[i] = [x.lemma_.strip() for x in tokens]

        tokens = model(row["text"])
        tokens = [
            x.lemma_.strip() for x in tokens if x.lemma_ not in "!-;:\"\'_/\\—,.?"
        ]

        for key in keywords:
            per = 0
            for i in range(len(tokens) - len(key) + 1):
                if tokens[i:i+len(key)] == key:
                    per += 1

            per = per/(len(tokens) - len(key) + 1)
            outputs.append(
                [
                    row["idx"],
                    ' '.join(key),
                    per if metric == 'float' else f"{per*100}%"
                ]
            )

    return pd.DataFrame(outputs, columns=['idx','key', 'frequency'])
