import os
import shutil

import pandas as pd
import wget
from malevich.square import APP_DIR, DF, Context, processor, scheme
from pydantic import BaseModel


@scheme()
class Links(BaseModel):
    link: str



@processor()
def download(links: DF[Links], context: Context):
    """Download files from the internet

    Inputs:
        A dataframe with a single column `link` containing links to files to download.

    Outputs:
        A dataframe with a single column `file` containing paths to downloaded files.

    Configuration:
        prefix (str, optional): a prefix to add to the paths of downloaded files.
            If not specified, files will be downloaded to the root of the app directory.

    Args:
        links (DF[Links]): Dataframe with links to download
        context (Context): Context object

    Returns:
        Dataframe with paths to downloaded files
    """
    prefix = context.app_cfg.get("prefix", "")
    try:
        os.makedirs(os.path.join(APP_DIR, prefix))
    except Exception as e:
        raise Exception(f"Could not use prefix: {prefix}. Use another") from e

    outputs = []

    for link in links.link:
        file = wget.download(link)

        shutil.move(file, os.path.join(APP_DIR, prefix, file))
        context.share(os.path.join(prefix, file))
        outputs.append(os.path.join(prefix, file))

    return pd.DataFrame({"file": outputs})
