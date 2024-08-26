from typing import Literal

import pandas as pd
from malevich.square import Context, Doc, Docs, processor, scheme
from pydantic import BaseModel, Field


@scheme()
class Reorient(BaseModel):
    orientation: Literal["column_index", "columns", "index"] = Field(..., title="Orientation")


@processor()
def reorient_one(document: Doc, context: Context[Reorient]) -> Doc:
    """Changes orientation of tabular document

    Orientations:

    1. Column index: {"column": {"index": {... data ...}}}
    2. Columns: {"column": [values]}
    3. Index: {"index": {"column": {... data ...}}}

    ## Input:
        A tabular document.

    ## Output:
        A document with a different orientation.

    ## Configuration:
        - `orientation`: string.
            The orientation of the document.
            Possible values: "column_index", "columns", "index".

    -----
    """
    return pd.DataFrame(document.dict()).to_dict(context.app_cfg.orientation)

@processor()
def reorient_many(documents: Docs, context: Context[Reorient]) -> Docs:
    """Changes orientation of a list of tabular documents

    Orientations:

    1. Column index: {"column": {"index": {... data ...}}}
    2. Columns: {"column": [values]}
    3. Index: {"index": {"column": {... data ...}}}

    ## Input:
        A list of tabular documents.

    ## Output:
        A list of documents with a different orientation.

    ## Configuration:
        - `orientation`: string.
            The orientation of the document.
            Possible values: "column_index", "columns", "index".

    -----
    """
    return [
        pd.DataFrame(document.dict()).to_dict(context.app_cfg.orientation)
        for document in documents
    ]

@processor()
def reorient_records(records: Docs, context: Context[Reorient]) -> Doc:
    """Changes orientation of a list of homogeneous records

    Orientations:

    1. Column index: {"column": {"index": {... data ...}}}
    2. Columns: {"column": [values]}
    3. Index: {"index": {"column": {... data ...}}}

    ## Input:
        A list of homogeneous records.

    ## Output:
        A document with a different orientation.

    ## Configuration:
        - `orientation`: string.
            The orientation of the document.
            Possible values: "column_index", "columns", "index".

    -----
    """
    return pd.DataFrame([record.dict() for record in records]).to_dict(
        context.app_cfg.orientation
    )
