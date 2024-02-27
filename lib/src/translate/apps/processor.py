import concurrent.futures

import pandas as pd
from googletrans import Translator
from malevich.square import DF, processor, scheme
from pydantic import BaseModel


@scheme()
class TextWithLanguageTranslationPairs(BaseModel):
    text: str
    from_language: str
    to_language: str


@processor()
def translate_texts(
    text_with_lang_pairs: DF['TextWithLanguageTranslationPairs'],
):
    """Translate texts from one language to another

    ## Input:
        A dataframe with the following columns:
            - `text` (str): text to translate
            - `from_language` (str): language code to translate from
            - `to_language` (str): language code to translate to

    ## Output:
        A dataframe with the following columns:
            - `text` (str): original text
            - `from_language` (str): language code to translate from
            - `to_language` (str): language code to translate to
            - `translation` (str): translated text in the target language

    ## Details:
        The app utilizes Google Translate API to translate texts.

        Columns `text`, `from_language`, and `to_language` are copied
        from the input dataframe without any modification.

    -----

    Args:
        docs (DF[TextWithLanguageTranslationPairs]):
            Input dataframe with texts to translate

    Returns:
        Dataframe with a column `translation` containing translated texts
        attached to the end of the input dataframe
    """

    translator = Translator()
    def process_row(row: pd.Series) -> str:
        return translator.translate(
            row['text'],
            src=row['from_language'],
            dest=row['to_language']
        ).text

    with concurrent.futures.ThreadPoolExecutor() as executor:
        translations = list(
            executor.map(process_row, text_with_lang_pairs.to_dict(orient='records')))

    output_df = text_with_lang_pairs.copy()
    output_df.insert(
        len(text_with_lang_pairs.columns), 'translation', translations
    )
    return output_df
