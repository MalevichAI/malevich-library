# generated by datamodel-codegen:
#   filename:  convert_pdf_to_jpeg_model.json

from __future__ import annotations

from typing import Optional

from malevich.square import scheme
from pydantic import BaseModel, Field


@scheme()
class ConvertPdfToJpeg(BaseModel):
    start_page: Optional[int] = Field(
        0,
        description='The number of the first page to convert. If not specified, converts from the first page',
    )
    page_num: Optional[int] = Field(
        None,
        description='The number of pages to convert. If not specified, converts all pages',
    )
