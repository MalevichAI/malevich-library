import fasttext
import pandas as pd
from malevich.square import DF, processor, scheme
from pydantic import BaseModel


@scheme()
class Text(BaseModel):
    text: str

def _prepare_text(text: str) -> str:
    text = text.replace('\n', ' ').replace('\r', ' ')
    text = text.replace('\t', ' ').replace('\v', ' ')
    return text


@processor()
def detect_language(texts: DF[Text]):
    """Detects language of provided text

    ## Input:

    A dataframe with column:
    - `text` (str): The text for detection.

    ## Output:
    A dataframe with columns:
    - `text` (str): Provided text
    - `language` (str): Detected language

    -----

    Args:
    texts (DF[Text]): DataFrame with texts

    Returns:
    A DataFrame with detection results.
    """
    model = fasttext.load_model('/model/lid.176.ftz')

    return pd.DataFrame(
        {
            'text': texts.text.to_list(),
            'language': [
                model.predict(_prepare_text(text))[0][0].replace('__label__', '')
                for text in texts.text.to_list()
            ]
        }
    )
