# generated by datamodel-codegen:
#   filename:  s3_save_files_model.json
#   timestamp: 2024-03-05T17:40:29+00:00

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class S3SaveFiles(BaseModel):
    append_run_id: Optional[bool] = Field(
        False, description='If True, the run_id is appended to the names of the files'
    )
    aws_access_key_id: str = Field(..., description='AWS access key ID')
    aws_secret_access_key: str = Field(..., description='AWS secret access key')
    bucket_name: str = Field(..., description='Name of the S3 bucket')
    endpoint_url: str = Field(..., description='Endpoint URL of the S3 bucket')
    aws_region: str = Field(..., description='AWS region of the S3 bucket')
