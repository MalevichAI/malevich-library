# S3 Save Component

## General Purpose

The S3 Save component is designed to facilitate the storage of tabular data by saving multiple dataframes to an Amazon S3 bucket. This component is particularly useful for persisting data in a cloud environment, ensuring that dataframes are securely stored and can be accessed or shared across different systems and processes.

## Input and Output Format

**Input Format:** The component accepts multiple dataframes packaged within a DataFrames Structure (DFS).

**Output Format:** The output of this component is the same as the input, meaning that the dataframes provided to the component are returned unchanged after being saved to S3.

## Configuration Parameters

| Parameter Name           | Expected Type        | Description |
| ------------------------ | -------------------- | ----------- |
| names                    | List of Strings / String | Optional. Names of the dataframes to be saved. Can be a list or a format string with `{ID}` as a placeholder for dataframe index. |
| append_run_id            | Boolean              | Optional. If `True`, appends the run ID to the names of the dataframes. Default is `False`. |
| extra_str                | String               | Optional. A string to be appended to the names of the dataframes. |
| aws_access_key_id        | String               | AWS access key ID for S3 authentication. |
| aws_secret_access_key    | String               | AWS secret access key for S3 authentication. |
| bucket_name              | String               | Name of the S3 bucket where dataframes will be saved. |
| endpoint_url             | String               | Optional. Endpoint URL of the S3 bucket. |
| aws_region               | String               | Optional. AWS region of the S3 bucket. |

## Detailed Configuration Parameters

- **names**: This parameter allows you to specify the names under which the dataframes will be saved in the S3 bucket. You can provide a list of names corresponding to each dataframe or a single string with a format placeholder `{ID}` which will be replaced by the dataframe's index. If the provided list is shorter than the number of dataframes, or if the string does not contain enough format placeholders, default names will be generated for the remaining dataframes.

- **append_run_id**: When set to `True`, this boolean flag will append the run ID to each dataframe name, ensuring uniqueness and traceability of data across different runs.

- **extra_str**: An optional string that, if provided, will be appended to the beginning of each dataframe name. This is useful for organizing dataframes into different directories or categories within your S3 bucket.

- **aws_access_key_id**, **aws_secret_access_key**, **bucket_name**: These parameters are required for S3 authentication and to specify the target bucket. They must be provided to allow the component to establish a connection with the S3 service.

- **endpoint_url**, **aws_region**: These optional parameters can be used to specify the endpoint URL and region of the S3 bucket, which might be necessary for certain configurations or when using S3-compatible services.

## Example Usage

When using this component, you would typically specify the names of the dataframes you wish to save, along with your AWS credentials and bucket details. If you want to organize your saved dataframes into a specific folder structure, you can use the `extra_str` parameter. For example, setting `extra_str` to "training_data" would result in dataframes being saved in a "training_data" folder within your S3 bucket, followed by the run ID and the specified dataframe name.