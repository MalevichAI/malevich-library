import os
import shutil

import pandas as pd
from malevich.square import APP_DIR, DF, Context, init, obj, processor, scheme
from pydantic import Field


@scheme()
class CollectAssetConfig:
    path_column_name: str = Field(
        'path', description='Name of the column containing the paths to the assets'
    )

@init()
def freeze_dir(ctx: Context):
    ctx.common = os.listdir(APP_DIR)

@processor()
def collect_asset(df: DF, context: Context[CollectAssetConfig]):
    paths = df[context.app_cfg.path_column_name].to_list()
    outputs = []
    for path in paths:
        os.makedirs(os.path.join(APP_DIR, path), exist_ok=True)
        shutil.copy(path, os.path.join(APP_DIR, path))
        outputs.append(path)
    context.share_many(outputs)
    return pd.DataFrame(outputs, columns=[context.app_cfg.path_column_name])
