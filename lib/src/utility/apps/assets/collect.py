import os
import shutil

import pandas as pd
from malevich.square import APP_DIR, DF, Context, init, obj, processor


@init()
def freeze_dir(ctx: Context):
    ctx.common = os.listdir(APP_DIR)

@processor()
def collect_asset(df: DF[obj], context: Context):
    """
    Moves assets to shared filesystem

    Input:
        An asset

    Output:
        A dataframe with a column:

        - `path' (str): A path (or paths) to asset files in the shared FS.

    -----
    """
    paths = df.path.to_list()
    outputs = []
    for path in paths:
        os.makedirs(os.path.join(APP_DIR, path), exist_ok=True)
        shutil.copy(path, os.path.join(APP_DIR, path))
        outputs.append(path)
    context.share_many(outputs)
    return pd.DataFrame(outputs, columns=['path'])


