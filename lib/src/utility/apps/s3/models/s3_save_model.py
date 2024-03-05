# generated by datamodel-codegen:
#   filename:  s3_save_model.json
#   timestamp: 2024-03-05T17:40:29+00:00

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class S3Save(BaseModel):
    names: List[str] = Field(..., description='Names of the dataframes to be saved')
    append_run_id: Optional[bool] = Field(
        False,
        description='If True, the run_id is appended to the names of the dataframes',
    )
    extra_str: str = Field(
        ..., description='If provided, it is appended to the names of the dataframes'
    )
    aws_access_key_id: str = Field(..., description='AWS access key ID')
    aws_secret_access_key: str = Field(..., description='AWS secret access key')
    bucket_name: str = Field(..., description='Name of the S3 bucket')
    endpoint_url: str = Field(..., description='Endpoint URL of the S3 bucket')
    aws_region: str = Field(..., description='AWS region of the S3 bucket')
