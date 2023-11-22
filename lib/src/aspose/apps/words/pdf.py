import os

import aspose.words as aw
import pandas as pd
from malevich.square import APP_DIR, DF, Context, processor, scheme
from pydantic import BaseModel


@scheme()
class Filename(BaseModel):
    filename: str


@processor()
def convert_pdf_to_markdown(files: DF[Filename], context: Context):
    """Convert PDF files to markdown.

    Input:
        A dataframe with a column named `filename` containing PDF files.

    Configuration:
        - write_contents (bool):
            If true, contents of the file will be produced in the
            output rather than just the path to the file.

    Output:
        The same dataframe with a column named `markdown` attached to the
        end. The column contains the path to the converted markdown files.

    Args:
        files (DF[Filename]):
            A dataframe with a column named `filename` containing PDF files.

    Returns:
        DF[Filename]:
            The same dataframe with a column named `markdown` attached to the
            end. The column contains the path to the converted markdown files.
    """
    outputs = []
    for filename in files.filename.to_list():
        doc = aw.Document(context.get_share_path(filename))
        result_path = os.path.basename(
            filename.replace(".pdf", ".md")
        )
        doc.save(
            os.path.join(
                APP_DIR,
                result_path
            ), aw.SaveFormat.MARKDOWN
        )

        context.share(result_path)
        if context.app_cfg.get("write_contents", False):
            with open(
                os.path.join(
                    APP_DIR,
                    result_path
                )
            ) as f:
                outputs.append(
                    f.read()
                )
        else:
            outputs.append(
                result_path
            )

    files.insert(
        len(files.columns),
        "markdown",
        pd.Series(outputs)
    )

    return files