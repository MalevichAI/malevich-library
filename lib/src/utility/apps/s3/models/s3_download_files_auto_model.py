# generated by datamodel-codegen:
#   filename:  s3_download_files_auto_model.json

from __future__ import annotations

from typing import Optional

from malevich.square import scheme
from pydantic import BaseModel, Field


@scheme()
class S3DownloadFilesAuto(BaseModel):
    aws_access_key_id: str = Field(..., description='AWS access key ID')
    aws_secret_access_key: str = Field(..., description='AWS secret access key')
    bucket_name: str = Field(..., description='Name of the S3 bucket')
    endpoint_url: Optional[str] = Field(
        None, description='Endpoint URL of the S3 bucket'
    )
    aws_region: Optional[str] = Field(None, description='AWS region of the S3 bucket')
