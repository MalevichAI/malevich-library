import os

import cv2
import pandas as pd
from malevich.square import APP_DIR, DF, Context, processor, scheme
from pydantic import BaseModel
from rembg import remove


@scheme()
class ImagePaths(BaseModel):
    path_to_image: str


@processor()
def remove_background(images: DF[ImagePaths], context: Context):
    """Removes background from image.

    Input:
        A dataframe with a column named `path_to_image` containing image path.

    Output:
        A dataframe with a column named `no_background_image` containing image path.

    Configuration:
        The app does not require any configuration.

    Args:
        images: A dataframe with a column named `path_to_image` containing image path.
        context: A context object.

    Returns:
        A dataframe with a column named `no_background_image` containing image path.
    """
    outputs = []
    for img in images.path_to_image.to_list():
        _file = context.get_share_path(img, not_exist_ok=True)
        if not os.path.exists(_file):
            outputs.append(img)
        else:
            _img = cv2.imread(_file)
            _nobg = remove(
                _img
            )
            # add _nobg before extention
            _base, _ = os.path.splitext(img)
            _base += "_nobg" + '.png'
            _path = os.path.join(APP_DIR, _base)
            cv2.imwrite(
                _path,
                _nobg
            )
            context.share(_base)
            context.synchronize([_base])
            outputs.append(_base)

    return pd.DataFrame(outputs, columns=['no_background_image'])

