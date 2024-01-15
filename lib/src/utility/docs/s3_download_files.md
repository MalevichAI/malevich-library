# S3 Download Files

## General Purpose

The "S3 Download Files" component is designed to facilitate the downloading of files from an Amazon S3 bucket to the local file system. It is intended for use within an AI-driven product development platform that provides a no-code experience. The component allows users to specify which files they wish to download using a simple tabular format.

## Input and Output Format

### Input Format
The input to this component is a dataframe with the following two columns:
- `filename`: The name of the file as it will be saved locally.
- `s3key`: The corresponding S3 key where the file is stored in the S3 bucket.

### Output Format
The output of this component is identical to the input dataframe. The files specified in the input are downloaded and made available locally, but the structure of the dataframe remains unchanged.

## Configuration Parameters

| Parameter Name           | Expected Type | Description                                           |
|--------------------------|---------------|-------------------------------------------------------|
| aws_access_key_id        | String        | AWS access key ID.                                    |
| aws_secret_access_key    | String        | AWS secret access key.                                |
| bucket_name              | String        | Name of the S3 bucket from which to download files.   |
| endpoint_url             | String        | (Optional) Endpoint URL of the S3 bucket.             |
| aws_region               | String        | (Optional) AWS region of the S3 bucket.               |

## Configuration Parameters Details

- **aws_access_key_id**: This is your AWS access key ID, which is part of your security credentials that allow you to access AWS services.
  
- **aws_secret_access_key**: This is your AWS secret access key, which is used in conjunction with the access key ID to sign programmatic requests to AWS.

- **bucket_name**: The name of the S3 bucket where your files are stored. This is a unique identifier for your bucket within AWS.

- **endpoint_url**: (Optional) The endpoint URL provides the address of the S3 service. This is useful if you are using a custom endpoint or a specific regional endpoint.

- **aws_region**: (Optional) This specifies the AWS region where your S3 bucket is located. It's important for the component to know the region to properly access the bucket.

## Detailed Behavior

When the "S3 Download Files" component is executed, it will download each file from the S3 bucket based on the `s3key` provided in the input dataframe. The downloaded files are saved locally with the names specified in the `filename` column. The component ensures that the files are available for subsequent processing steps in the pipeline. 

For instance, if the input dataframe contains a row with `filename` as `file1.csv` and `s3key` as `path/to/some_file.csv`, the component will download the file from the S3 bucket located at `path/to/some_file.csv` and save it locally as `file1.csv`.

This component does not alter the structure of the input dataframe; it simply performs the action of downloading the specified files and ensures that they are available for further use within the platform's pipeline.