# S3 Save Files

## General Component Purpose

The "S3 Save Files" component is designed to transfer files from a local file system to an Amazon S3 bucket. This operation is crucial for storing data backups, sharing files across different systems, or making data accessible for further processing in cloud-based applications. The component ensures that files are securely and efficiently uploaded to a specified S3 bucket.

## Input and Output Format

### Input Format

The input for this component is a dataframe with two columns:

- `filename`: The name of the file to be saved.
- `s3key`: The S3 key that will be assigned to the file upon saving.

### Output Format

The output of this component is identical to the input. The dataframe is returned unchanged, serving as a confirmation of the files processed.

## Configuration Parameters

| Parameter Name           | Expected Type | Description                                           |
|--------------------------|---------------|-------------------------------------------------------|
| append_run_id            | Boolean       | If true, appends the run_id to the file names.        |
| aws_access_key_id        | String        | AWS access key ID for authentication.                 |
| aws_secret_access_key    | String        | AWS secret access key for authentication.             |
| bucket_name              | String        | The name of the S3 bucket where files will be saved.  |
| endpoint_url             | String        | Optional. The endpoint URL of the S3 bucket.          |
| aws_region               | String        | Optional. The AWS region where the S3 bucket resides. |

## Detailed Configuration Parameters

- **append_run_id**: When set to true, the unique identifier of the run (`run_id`) is appended to the names of the files, which can be useful for versioning and tracking purposes.

- **aws_access_key_id**: This is your AWS access key ID, which is used to authenticate and authorize the file upload process.

- **aws_secret_access_key**: This is your AWS secret access key, which works in conjunction with the access key ID to ensure secure access to your S3 bucket.

- **bucket_name**: The name of the S3 bucket where you want to save your files. This should be pre-existing and accessible with the provided AWS credentials.

- **endpoint_url** (optional): The endpoint URL provides the address of the S3 bucket. This is particularly useful if you are using a custom or private S3 endpoint.

- **aws_region** (optional): The AWS region parameter specifies the geographical region where your S3 bucket is hosted. This can affect the latency and availability of the service.

## How It Works

Files must be placed in the shared folder and shared with the context using `context.share(<FILE>)` by a previous processor. The files are then saved to the S3 bucket using the specified key pattern. You can use variables such as `{ID}`, `{FILE}`, and `{RUN_ID}` within the S3 key to dynamically create the file path in the bucket.

For instance, if you set the `extra_str` as 'train', and your S3 key pattern is 'train/{RUN_ID}/{FILE}', a file named 'file.csv' with a `run_id` of 'run_1' will be saved to 'train/run_1/file.csv' in the S3 bucket.

This component is essential for workflows that require the storage of files in a cloud environment, enabling seamless data management and accessibility.