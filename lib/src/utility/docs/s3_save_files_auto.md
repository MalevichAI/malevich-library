# S3 Save Files Auto

## General Purpose

This component is designed to save files from the local file system to an Amazon S3 bucket, maintaining the original file names. It can be configured to append additional strings or identifiers to the file names before saving, which is useful for organizing files within the S3 bucket.

## Input Format

The input to this component is a dataframe with a single column:

- `filename`: A column containing the names of the files that need to be saved to S3.

## Output Format

The output of this component is the same dataframe as the input, with the addition of a column `s3key` that contains the S3 keys of the saved files.

## Configuration Parameters

| Parameter Name          | Expected Type | Description |
| ----------------------- | ------------- | ----------- |
| append_run_id           | Boolean       | Optional. If set to True, the run ID is appended to the file names. Default is False. |
| extra_str               | String        | Optional. A string to append to the file names. |
| aws_access_key_id       | String        | The AWS access key ID for S3 access. |
| aws_secret_access_key   | String        | The AWS secret access key for S3 access. |
| bucket_name             | String        | The name of the S3 bucket where files will be saved. |
| endpoint_url            | String        | Optional. The endpoint URL of the S3 bucket. |
| aws_region              | String        | Optional. The AWS region where the S3 bucket is located. |

## Detailed Configuration Parameters

- **append_run_id**: When enabled, this option appends the unique run identifier to each file name, which helps in distinguishing between different runs or sessions.

- **extra_str**: This string is appended to the file name and can be used to categorize files into different folders within the S3 bucket. For example, setting `extra_str` to "train" would save the files under a "train" folder in the specified S3 bucket.

- **aws_access_key_id**: This is your AWS access key ID, which is required to authenticate and authorize the file-saving operation to the specified S3 bucket.

- **aws_secret_access_key**: This is your AWS secret access key, which works in conjunction with the access key ID to ensure secure access to your S3 resources.

- **bucket_name**: This is the name of the S3 bucket where the files will be saved. It is essential to specify the correct bucket name to ensure that the files are stored in the intended location.

- **endpoint_url**: This is the endpoint URL of the S3 bucket. It is an optional parameter that can be used when working with S3-compatible services or when the S3 bucket is not in the standard AWS endpoint.

- **aws_region**: This optional parameter specifies the AWS region of the S3 bucket. It is important for the component to know the region to correctly interact with the S3 service.

## Usage Notes

Before using this component, ensure that the files to be saved are available in the shared folder and have been shared using the `context.share(<FILE>)` method by a previous processor. The component constructs the S3 key for each file based on the configuration parameters and saves each file to the S3 bucket using the constructed key.