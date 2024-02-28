import concurrent
import os
from typing import Optional
from uuid import uuid4

import pandas as pd
from gtts import gTTS
from malevich.square import APP_DIR, DF, Context, processor, scheme
from pydantic import BaseModel


@processor()
def text_to_speech(texts: DF['TextWithLanguageCode'], context: Context):
    """Convert text to speech

    ## Input:
        A dataframe with columns:
        - `text` (str): text to be converted.
        - `language` (str, optional): language of the text, will use english by default

    ## Output:
        A dataframe with a column:
        - `speech` (str): path to converted audio.

    -----

    Args:
        - texts (DF[TextWithLanguageCode]): DataFrame with text

    Returns:
        A DataFrame with audio filenames.
    """
    def process_row(row):  # noqa: ANN202
        language = 'en' if 'language' not in row else row['language']
        tts = gTTS(text=row['text'], lang=language)
        id = uuid4().hex
        mp3_path = os.path.join(APP_DIR, f'{id}.mp3')
        tts.save(mp3_path)
        context.share(f'{id}.mp3')
        return f'{id}.mp3'

    with concurrent.futures.ThreadPoolExecutor() as executor:
        speech = list(executor.map(process_row, texts.to_dict(orient='records')))

    return pd.DataFrame({'speech': speech})



@scheme()
class TextWithLanguageCode(BaseModel):
    text: str
    language: Optional[str] = 'en'
