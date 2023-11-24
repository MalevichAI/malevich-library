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
