import fasttext
import pandas as pd
from pydantic import BaseModel
from malevich.square import DF, processor, scheme


@scheme()
class Text(BaseModel):
    text: str


@processor()
def detect_language(texts: DF[Text]):
    model = fasttext.load_model('/model/lid.176.ftz')

    return pd.DataFrame(
        {
            'text': texts.text.to_list(),
            'language': [
                model.predict(text)[0][0].replace('__label__', '')
                for text in texts.text.to_list()
            ]
        }
    )
