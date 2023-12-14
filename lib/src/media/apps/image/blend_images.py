import os

import pandas as pd
from malevich.square import APP_DIR, DF, Context, processor, scheme
from PIL import Image
from pydantic import BaseModel


def _blend_images(background_path, object_path, output_path):
    # Open the images
    background = Image.open(background_path)

    # Open in RGBA mode to support transparency
    object_image = Image.open(object_path).convert('RGBA')

    # Calculate the position to center the object on the background
    bg_width, bg_height = background.size
    obj_width, obj_height = object_image.size

    x = (bg_width - obj_width) // 2
    y = (bg_height - obj_height) // 2

    # Create a new image with the background size and mode
    blended_image = Image.new('RGBA', background.size)

    # Paste the background and object onto the new image
    blended_image.paste(background, (0, 0))
    blended_image.paste(object_image, (x, y), object_image)

    # Save the blended image
    blended_image.save(output_path, 'PNG')  # Save as PNG to retain transparency

@scheme()
class TwoImages(BaseModel):
    background_image_path: str
    patch_image_path: str


@processor()
def blend_images(images: DF[TwoImages], context: Context):
    """Roughly blends two images by overlaying one on top of another

    Inputs:
        A dataframe with two columns: `background_image_path` and `patch_image_path`.
        Each row of the dataframe will be used to blend two images. For example, if your
        background image is `background.png` and your patch image is `patch.png`, then
        the output image will be an original background image with a patch image on top
        of it.

    Outputs:
        A dataframe with one column `blended` with paths to blended images.

    Configuration:
        There is no configuration for this processor.

    Args:
        images (DF[TwoImages]): Dataframe with paths to images
        context (Context): Context object

    Returns:
        Dataframe with paths to blended images
    """
    outputs = []
    for _, row in images.iterrows():
        background_path = str(row['background_image_path'])
        patch_path = str(row['patch_image_path'])
        try:
            bg_real_path = context.get_share_path(background_path)
            patch_real_path = context.get_share_path(patch_path)
        except Exception as e:
            raise Exception(
                "Could not find files. Please, ensure that both columns contain files "
                "previously shared within previous processors"
            )
        output_path = f'{patch_path}_on_{background_path}.png'
        output_real_path = os.path.join(APP_DIR, output_path)

        _blend_images(bg_real_path, patch_real_path, output_real_path)
        print(os.path.exists(output_real_path))
        print(os.listdir(APP_DIR))
        context.share(output_path)
        context.synchronize([output_path])

        outputs.append(output_path)

    return pd.DataFrame(outputs, columns=['blended'])

