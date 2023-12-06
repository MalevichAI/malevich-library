import os
import shutil

import gdown
import pandas as pd
from malevich.square import APP_DIR, DF, Context, processor, scheme
from pydantic import BaseModel

# from mosaic.files.assertfile import assertfile


@scheme()
class GoogleDriveLink(BaseModel):
    link: str

# @assertfile(output_column="filename")
@processor()
def download_from_google_drive(links: DF[GoogleDriveLink], context: Context):
    """Download files from google drive.

    Input:
        A dataframe with a column named `link` containing google drive links.

    Configuration:
        - fail_on_error: bool, default False.
            If True, the app will fail if any of the links are invalid.

    Output:
        A dataframe with a column named `filename` containing the downloaded files
        shared across all apps.

    Args:
        links (DF[GoogleDriveLink]):
            A dataframe with a column named `link` containing google drive links.

    Returns:
        DF[Filename]:
            A dataframe with a column named `filename`
            containing the downloaded files shared across all apps.
    """
    outputs = []
    for link in links.link.to_list():
        if 'folder' not in link:
            try:
                output_file = gdown.download(
                    link,
                    fuzzy=True,
                    quiet=True
                )

                basename = os.path.basename(output_file)

                shutil.copyfile(
                    output_file,
                    os.path.join(
                        APP_DIR,
                        basename
                    )
                )

                outputs.append(
                    basename
                )
            except Exception as e:
                if context.app_cfg.get("fail_on_error", False):
                    raise e
                else:
                    print(f"Failed to download {link}")
                    print(e)
        else:
            try:
                output_files = gdown.download_folder(
                    link,
                    quiet=True
                )

                for output_file in output_files:
                    basename = os.path.basename(output_file)

                    shutil.copyfile(
                        output_file,
                        os.path.join(
                            APP_DIR,
                            basename
                        )
                    )

                    outputs.append(
                        basename
                    )
            except Exception as e:
                if context.app_cfg.get("fail_on_error", False):
                    raise e
                else:
                    print(f"Failed to download {link}")
                    print(e)

    context.share_many(
        outputs
    )

    outputs = [
        output_file.replace(APP_DIR, '').lstrip('/') for output_file in outputs
    ]

    return pd.DataFrame(
        outputs,
        columns=["filename"]
    )
