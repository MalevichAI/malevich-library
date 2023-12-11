import os

import pandas as pd
from malevich.square import APP_DIR, DF, Context, processor, scheme
from PIL import Image
from pydantic import BaseModel


@scheme()
class ImageSchema(BaseModel):
    filename: str


@processor()
def resize(df: DF[ImageSchema], context: Context):
    """Resizes images and reformats them

    Input:
        A dataframe with a column named `filename` containing image path.

    Output:
        A dataframe with a column named `filename` containing image path.

    Configuration:
        - width: int, default None.
            The width of the resized image.
        - height: int, default None.
            The height of the resized image.
        - preserve_ratio: bool, default True.
            If True, the aspect ratio of the image will be preserved.
        - image_type: str, default "jpg".
            The type of the image. Beware that some
            reformats may not support transparency.

    Args:
        df (DF[ImageSchema]):
            A dataframe with a column named `filename` containing image path.
        context (Context):
            A context object.

    Returns:
        A dataframe with a column named `filename` containing image path.
    """
    width = context.app_cfg.get('width', None)
    height = context.app_cfg.get('height', None)
    preserve_ratio = context.app_cfg.get('preserve_ratio', True)
    im_type = context.app_cfg.get('image_type', "jpg")
    outputs = []
    for _, row in df.iterrows():
        filepath = context.get_share_path(str(row['filename']))
        img = Image.open(filepath)
        if preserve_ratio:
            ratio = img.width / img.height
            if width is not None and height is None:
                height = int(width / ratio)
            elif height is not None and width is None:
                width = int(height * ratio)
            elif height is None and width is None:
                width = img.width
                height = img.height
        else:
            width = width or img.width
            height = height or img.height
        img = img.resize((width, height))

        new_filename = os.path.basename(
            os.path.splitext(row['filename'])[0] + f'_compressed.{im_type}'
        )
        try:
            img = img.convert('RGBA')
            img.save(
                os.path.join(
                    APP_DIR,
                    new_filename
                )
            )
        except OSError:
            try:
                img = img.convert('RGB')
                img.save(
                    os.path.join(
                        APP_DIR,
                        new_filename
                    )
                )
            except Exception as e:
                raise Exception(f"Could not save file: {e}")

        context.share(new_filename)
        context.synchronize([new_filename])
        outputs.append(new_filename)

    return pd.DataFrame(outputs, columns=['filename'])
