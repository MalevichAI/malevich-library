import os

import pandas as pd
from malevich.square import APP_DIR, DF, Context, processor, scheme
from PIL import Image
from pydantic import BaseModel


@scheme()
class ImageSchema(BaseModel):
    filename:str

@processor()
def compress_img(df: DF[ImageSchema], context: Context):
    width = context.app_cfg.get('width', None)
    height = context.app_cfg.get('height', None)
    im_type = context.app_cfg.get('image_type', "jpg")
    outputs = []
    for _, row in df.iterrows():
        filepath = context.get_share_path(row['filename'])
        img = Image.open(filepath)
        new_width = img.width if width is None else width
        new_height = img.height if height is None else height
        img = img.resize((new_width, new_height))
        new_filename = os.path.basename(
                os.path.splitext(row['filename'])[0] + f'.{im_type}'
            )
        if im_type == 'jpg' and img.mode == 'RGBA':
            img = img.convert('RGB')
        img.save(
            os.path.join(
                APP_DIR,
                new_filename
            )
        )
        context.share(new_filename, all_runs=True)
        outputs.append(new_filename)

    return pd.DataFrame(outputs, columns=['filename'])
