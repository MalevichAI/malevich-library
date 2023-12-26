import fasttext
import pandas as pd
from malevich.square import DF, processor, scheme
from pydantic import BaseModel


@scheme()
class Text(BaseModel):
    text: str

def _prepare_text(text: str):
    text = text.replace('\n', ' ').replace('\r', ' ')
    text = text.replace('\t', ' ').replace('\v', ' ')
    return text


@processor()
def detect_language(texts: DF[Text]):
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
