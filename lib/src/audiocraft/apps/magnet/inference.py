import os

import pandas as pd

# from audiocraft.data.audio import audio_write
# from audiocraft.models import MAGNeT
import replicate
import wget
from malevich.square import APP_DIR, DF, OBJ, Context, init, processor, scheme


@scheme()
class Prompt:
    """
    A prompt for generating audio.
    """
    text: str

# @init()
# def init_magnet(context: Context):
#     model_name = context.app_cfg.get('model_name', 'facebook/audio-magnet-small')
#     context.common = MAGNeT.get_pretrained(model_name)


@processor()
def generate_audio(prompt: DF[Prompt], context: Context) -> str:
    """
    Generate audio from text.

    ## Input:
        A dataframe with column:
        - `text` (str): prompt to generate audio.

    ## Output:
        A dataframe with columns:
        - `audio_path` (str): path to the audio.
        - `description` (str): description of the audio.

    ## Configuration:

        - `replicate_api_key`: string.

            [Replicate](https://replicate.com/) API key.

        - `save_prefix`: string.

            Prefix path to save the audio in.

    -----

    Args:
        prompt: Dataframe with prompts.

    Returns:
        A DataFrame with audio info.
    """
    if "replicate_api_key" not in context.app_cfg:
        raise ValueError("replicate_api_key not set in configuration")
    os.environ['REPLICATE_API_TOKEN'] = context.app_cfg['replicate_api_key']
    # magnet: MAGNeT = context.common
    save_prefix = context.app_cfg.get('save_prefix', 'magnet/{RUN_ID}')
    save_prefix = save_prefix.format(RUN_ID=context.run_id)
    descriptions = prompt.text.to_list()
    # audio = magnet.generate(descriptions)
    audio_paths = []
    for idx, description in enumerate(descriptions):
        apath_ = os.path.join(APP_DIR, f'{save_prefix}/{idx}.wav')
        os.makedirs(os.path.dirname(apath_), exist_ok=True)
        output = replicate.run(
           "lucataco/magnet:e8e2ecd4a1dabb58924aa8300b668290cafae166dd36baf65dad9875877de50e",
            input={
                "prompt": description,
                "variations": 1
            }
        )
        wget.download(output[0], apath_)
        context.logger.info(f'[OK ] {apath_}')
        audio_paths.append(f'{save_prefix}/{idx}.wav')

    context.share_many(audio_paths)
    context.synchronize(audio_paths)

    return pd.DataFrame({'audio_path': audio_paths, 'description': descriptions})
