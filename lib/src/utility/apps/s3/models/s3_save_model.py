# generated by datamodel-codegen:
#   filename:  s3_save_model.json

from __future__ import annotations

from typing import List, Optional, Union

from malevich.square import scheme
from pydantic import BaseModel, Field


@scheme()
class S3Save(BaseModel):
    names: Union[List[str], str] = Field(
        ..., description='Names of the dataframes to be saved'
    )
    append_run_id: Optional[bool] = Field(
        False,
        description='If True, the run_id is appended to the names of the dataframes',
    )
    extra_str: Optional[str] = Field(
        None, description='If provided, it is appended to the names of the dataframes'
    )
    aws_access_key_id: str = Field(..., description='AWS access key ID')
    aws_secret_access_key: str = Field(..., description='AWS secret access key')
    bucket_name: str = Field(..., description='Name of the S3 bucket')
    endpoint_url: Optional[str] = Field(
        None, description='Endpoint URL of the S3 bucket'
    )
    aws_region: Optional[str] = Field(None, description='AWS region of the S3 bucket')
