import os

import aspose.words as aw
import pandas as pd
from malevich.square import APP_DIR, DF, Context, processor, scheme
from pydantic import BaseModel

from .models import ConvertPdfToJpg


@scheme()
class Filename(BaseModel):
    filename: str


@processor()
def convert_pdf_to_jpg(files: DF[Filename], context: Context[ConvertPdfToJpg]):
    """Convert PDF files to jpeg.

    ## Input:
        A dataframe with columns:
        - `filename` (str): containing PDF files.

    ## Configuration:
        - `start_page`: int, default 0.
            From which page to start.

        - `page_num`: int, default 0.
            Number of pages to retrieve.

    ## Output:
        The same dataframe with columns:
        - `filename` (str): containing PDF files.
        - `jpeg` (str): converted images.

    -----

    Args:
        files (DF[Filename]):
            A dataframe with a column named `filename` containing PDF files.

    Returns:
        DF[Filename]:
            The same dataframe with a column named `jpeg` attached to the
            end. The column contains the path to the converted jpeg files.
    """  # noqa: E501
    outputs = []
    start_page = context.app_cfg.get('start_page', 0)
    page_num = context.app_cfg.get('page_num', None)
    for filename in files.filename.to_list():
        doc = aw.Document(context.get_share_path(filename))
        pages = []
        for i in range(start_page,
                       min(
                           doc.page_count if page_num is None else start_page+page_num,
                           doc.page_count)
                        ):
            page = doc.extract_pages(i, 1)
            result_path = os.path.basename(
                filename.replace(".pdf", f"_{i+1}.jpg")
            )
            page.save(
                os.path.join(
                    APP_DIR,
                    result_path
                ), aw.SaveFormat.MARKDOWN
            )
            context.share(result_path)
            pages.append(
                result_path
            )
        df = pd.DataFrame({
                    'image': pages
                })
        df.insert(1, 'filename', filename)
        outputs.append(df)

    return pd.concat(outputs)
