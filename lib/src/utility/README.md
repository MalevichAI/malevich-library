# Pass Through Component

## General Purpose

The Pass Through component is designed to serve as a straightforward conduit within a product pipeline. Its primary function is to receive tabular data and pass it through without making any modifications. This component can be particularly useful for preserving the data flow structure in a pipeline or for testing purposes where the unaltered data needs to be examined downstream.

## Input and Output Format

**Input Format:** The component accepts tabular data in a standardized format that is compatible with the platform's data handling conventions.

**Output Format:** The output of this component is identical to the input - tabular data in the same format as it was received.

## Configuration Parameters

The Pass Through component does not require any configuration parameters, as it is designed to simply pass the data through without any changes.

## Detailed Parameter Descriptions

Since the Pass Through component does not alter the data, there are no configuration parameters to describe. It is a plug-and-play component that requires no additional setup or customization.

# Get Links to Files

## General Component Purpose

The "Get Links to Files" component is designed to transform tabular data by converting file paths within the data to openable links. This process facilitates the access to files produced during the workflow execution, making it easier for users to retrieve and view these files directly from the data table.

## Input and Output Format

**Input Format:** The component accepts an arbitrary dataframe with one or more columns that may contain file paths.

**Output Format:** The output is the same dataframe that was inputted, but with all file paths replaced with links that can be opened directly. These links will point to the actual files, allowing users to access them conveniently.

## Configuration Parameters

| Name         | Type | Description                                         |
|--------------|------|-----------------------------------------------------|
| expiration   | Int  | The number of seconds until the link will expire.   |

## Configuration Parameters Details

- **expiration**: This parameter sets the lifespan of the generated links. By default, links will expire after 6 hours, but this can be adjusted to any value up to a maximum of 24 hours. The time is specified in seconds. If not set, the default expiration time will be used.

## Usage Notes

- The generated links will be active for the duration specified by the `expiration` parameter. After this period, the links will no longer be accessible.
- It is important to ensure that the expiration time is set according to the needs of the users, considering the time they may require to access the files.
- This component is particularly useful in workflows where file access is needed post-processing, such as in reporting or data review stages.

Remember, this component helps streamline the process of file access within your data pipelines, enhancing the overall user experience by providing immediate access to the necessary files.

# Unwrap Component

## General Purpose

The Unwrap component is designed to expand tabular data where certain columns contain multiple values separated by a delimiter into multiple rows. Each row is a permutation of the original row with one of the multiple values in the specified columns. This is particularly useful for normalizing data and ensuring that each row represents a single record with atomic values.

## Input and Output Format

### Input Format

The input to this component is a dataframe with one or more columns that contain multiple values separated by a delimiter.

### Output Format

The output is a dataframe with the same columns as the input dataframe. However, for each row in the input, there will be multiple rows in the output, each containing one of the values from the multi-valued columns.

## Configuration Parameters

| Parameter  | Type             | Description                                           |
|------------|------------------|-------------------------------------------------------|
| columns    | List of Strings  | The columns to unwrap. Defaults to all columns.       |
| delimiter  | String           | The delimiter used to separate values in the columns. |

## Detailed Configuration Parameters

- **columns**: This is a list of column names from the dataframe that you wish to unwrap. If this parameter is not specified, the component will attempt to unwrap all columns.

- **delimiter**: This is the string that separates the multiple values within the columns. The default delimiter is a comma (`,`). It is important to choose a delimiter that does not appear in the single values of the columns to avoid incorrect unwrapping.

## Notes

- When using the Unwrap component, ensure that the delimiter chosen does not conflict with the actual data within the columns. For example, if the delimiter is set to a period (`.`) and the data contains floating-point numbers, this could result in unintended splitting of the number into separate values.

- The Unwrap component is particularly useful in scenarios where data normalization is required, such as preparing data for machine learning models or when performing data analysis tasks that require one record per row.

# Match Pattern

## General Purpose

The "Match Pattern" component is designed to process tabular data by identifying and extracting fragments within each cell that match a specified pattern. Once these fragments are found, they are concatenated together using a specified character and placed back into their respective cells, effectively transforming the data based on the pattern recognition.

## Input and Output Format

The input for this component is a dataframe with any number of columns and rows. Each cell in the dataframe should contain text data for the pattern matching to be performed.

The output is a new dataframe of the same dimensions and column names as the input. Each cell in the output dataframe contains the concatenated fragments that matched the specified pattern.

## Configuration Parameters

| Parameter Name | Expected Type       | Description                                           |
|----------------|---------------------|-------------------------------------------------------|
| pattern        | String              | The pattern to match within each cell of the dataframe.|
| join_char      | String (optional)   | The character used to join matched fragments.         |

## Configuration Parameters Details

- **pattern**: This is the specific sequence of characters that the component will search for within each cell of the dataframe. The pattern should be provided as a string and can include regular expression syntax to match a variety of text fragments.

- **join_char**: This optional parameter defines the character that will be used to concatenate the matched fragments found in each cell. If not specified, a default character will be used. The join character should be provided as a single string character.

## Usage Notes

- The component operates on string-type columns within the dataframe. Non-string columns will be ignored during the pattern matching process.
- The pattern matching is case-sensitive, and the pattern must be specified accurately to ensure correct matches.
- The resulting dataframe maintains the original structure, with the transformation applied only to the content of the cells.

Remember, no coding knowledge is required to configure and use this component. By specifying the desired pattern and join character, you can easily manipulate and transform your tabular data to better suit your analysis or reporting needs.

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

# Filter Component

## General Purpose

The Filter Component is designed to refine and reduce the data in a tabular format based on specified conditions. It allows users to apply various filtering operations to select only the rows that meet certain criteria. This component is essential for data preprocessing, enabling users to focus on relevant data and exclude the unnecessary or irrelevant entries.

## Input and Output Format

**Input Format**: The input for the Filter Component is an arbitrary dataframe that you wish to filter.

**Output Format**: The output is a dataframe that contains only the rows that meet the specified filtering conditions.

## Configuration Parameters

| Name       | Expected Type      | Description                                           |
|------------|--------------------|-------------------------------------------------------|
| conditions | List of Dictionaries | A list of conditions that specify the filtering criteria. |

## Configuration Parameters Details

- **conditions**: This is a list where each item is a dictionary that defines a single filtering condition. Each dictionary can have the following keys:
  - **column**: The name of the column in the dataframe to apply the filter on.
  - **operation**: The operation to use for filtering (e.g., 'equal', 'greater', 'less', 'like', etc.).
  - **value**: The value to compare against when filtering.
  - **type** (optional): The data type of the value (e.g., 'int', 'float', 'bool', 'str'). If not specified, 'str' is assumed.

### Supported Operations

- **equal**: Select rows where the column value is equal to the specified value.
- **not_equal**: Select rows where the column value is not equal to the specified value.
- **greater**: Select rows where the column value is greater than the specified value.
- **greater_equal**: Select rows where the column value is greater than or equal to the specified value.
- **less**: Select rows where the column value is less than the specified value.
- **less_equal**: Select rows where the column value is less than or equal to the specified value.
- **in**: Select rows where the column value is in a list of specified values.
- **not_in**: Select rows where the column value is not in a list of specified values.
- **like**: Select rows where the column value contains the specified substring.
- **not_like**: Select rows where the column value does not contain the specified substring.
- **is_null**: Select rows where the column value is null.
- **is_not_null**: Select rows where the column value is not null.

### Supported Types

- **int**: Integer type.
- **float**: Floating point number type.
- **bool**: Boolean type.
- **str**: String type.

The Filter Component is a powerful tool for data manipulation, allowing users to easily refine their datasets without writing any code. By configuring the conditions appropriately, users can create complex filters to process their data efficiently.

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

# Combine Vertical

## General Purpose

The "Combine Vertical" component is designed to concatenate two tabular data sets vertically. This operation is akin to appending the rows of one table to another, assuming both tables have the same number of columns. This component is useful when you want to merge data from two different sources that share the same column structure, or when you're consolidating records that have been split across multiple data sets.

## Input and Output Format

### Input Format
- **Dataframe1**: A Pandas DataFrame.
- **Dataframe2**: Another Pandas DataFrame with an equal number of columns as Dataframe1.

### Output Format
- A single Pandas DataFrame that represents the vertical concatenation of Dataframe1 and Dataframe2.

## Configuration Parameters

| Parameter Name     | Expected Type | Description                                                                 |
|--------------------|---------------|-----------------------------------------------------------------------------|
| ignore_col_names   | Boolean       | Determines whether to ignore the column names of the input dataframes.      |
| default_name       | String        | The template for generating column names if `ignore_col_names` is `True`.   |
| ignore_index       | Boolean       | Determines whether to ignore the index of the dataframes during concatenation. |

## Detailed Parameter Descriptions

- **ignore_col_names**: When set to `True`, the component will disregard the existing column names from both input dataframes and will generate new column names using the `default_name` parameter followed by an index (e.g., `col_1`, `col_2`, etc.). When set to `False`, it will attempt to preserve shared column names and only replace mismatched names with the generic template.

- **default_name**: This is the base name that will be used to generate new column names if `ignore_col_names` is `True`. For example, if `default_name` is set to "feature", the new column names will be "feature_1", "feature_2", and so on.

- **ignore_index**: If `True`, the component will ignore the index of the dataframes during the concatenation process, which means the resulting dataframe will have a new integer index starting from 0. If `False`, the original indices of the input dataframes will be preserved in the concatenated dataframe.

## Notes

- It is important that both input dataframes have the same number of columns. If they do not, the component will raise an error.
- The default behavior is to preserve column names and indices unless specified otherwise in the configuration.

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

# Subset Component

## General Purpose

The Subset component is designed to select specific portions of data from a collection of dataframes. This component is useful when you need to work with only a particular subset of your data, which can be specified using indices or ranges. It is ideal for scenarios where filtering data is necessary before applying further transformations or analyses.

## Input and Output Format

**Input Format:** The component accepts a collection of dataframes. Each dataframe should be in a tabular format.

**Output Format:** The component outputs either a single dataframe or a subset of dataframes based on the specified configuration.

## Configuration Parameters

| Name | Type | Description |
| ---- | ---- | ----------- |
| expr | String | A comma-separated list of integers or slices to specify the subset of dataframes to select. |

## Configuration Parameters Details

- **expr**
  - **Type:** String
  - **Description:** This parameter should contain a comma-separated list of integers or slices, which define the indices of the dataframes to be selected. For example, `0,1:3,5:7,6,9:10` indicates that the first dataframe (index 0), dataframes from index 1 to 2 (1:3), from 5 to 6 (5:7), the single dataframe at index 6, and from 9 to 9 (9:10) should be selected. Zero-based indexing is used, meaning the first dataframe has an index of 0. The format of this string must match the regular expression `^(\\d+|(\\d+\\:\\d+))(\\,(\\d+|(\\d+\\:\\d+)))*$`. If only one index or range is specified, a single dataframe is returned. If multiple indices or ranges are specified, a subset of dataframes is returned.

## Usage Notes

- Ensure that the `expr` configuration parameter is set correctly to avoid errors. It is crucial for specifying which dataframes to include in the output.
- The indices and ranges in the `expr` parameter should be separated by commas without spaces.
- If you need to select a continuous range of dataframes, use the slice notation with a colon (e.g., `1:4` to select dataframes with indices 1, 2, and 3).
- If the subset specified in `expr` results in only one dataframe, the output will be that single dataframe. Otherwise, the output will be a list of dataframes.

This component simplifies the process of selecting specific dataframes from a larger set, making it easier to focus on relevant data without the need for complex coding.

# Locate Statically Component

## General Purpose

The Locate Statically component is designed to extract specific subsets of data from a larger tabular dataset. It allows users to select particular rows and columns based on their names, indexes, or a combination of both. This component is useful when you need to focus on a certain part of your data for further analysis or processing.

## Input and Output Format

- **Input Format**: The component accepts a tabular dataset, commonly referred to as a DataFrame.
- **Output Format**: The output is a subset of the input DataFrame, containing only the selected rows and columns.

## Configuration Parameters

| Parameter Name | Expected Type       | Description                                           |
| -------------- | ------------------- | ----------------------------------------------------- |
| `column`       | String              | The name of the single column to be extracted.        |
| `columns`      | List of Strings     | The names of multiple columns to be extracted.        |
| `column_idx`   | Integer             | The index of a single column to be extracted.         |
| `column_idxs`  | List of Integers    | The indexes of multiple columns to be extracted.      |
| `row`          | Integer             | The index of a single row to be extracted.            |
| `rows`         | List of Integers    | The indexes of multiple rows to be extracted.         |
| `row_idx`      | Integer             | The index of a single row to be extracted.            |
| `row_idxs`     | List of Integers    | The indexes of multiple rows to be extracted.         |

## Detailed Configuration Parameters

- **`column`**: Specify the name of a single column to extract from the DataFrame. This is useful when you are interested in one specific column.

- **`columns`**: Provide a list of column names if you need to extract multiple columns. This is useful for analyzing or comparing specific features within your dataset.

- **`column_idx`**: Use this parameter to select a column by its index rather than its name. This can be handy when working with unnamed columns or when the name is not known.

- **`column_idxs`**: Similar to `column_idx`, but allows for selection of multiple columns by their indexes.

- **`row`**: This parameter allows you to select a single row from the DataFrame based on its index.

- **`rows`**: If you need to extract multiple rows, provide their indexes in a list. This is useful for extracting specific records.

- **`row_idx`**: Select a single row using its index. This is useful when you need to analyze or manipulate a specific entry in your dataset.

- **`row_idxs`**: A list of row indexes to extract multiple rows at once.

Please note that at least one of the above configuration parameters must be provided for the component to function properly. The extraction process prioritizes specificity; if both specific (single row/column) and general (multiple rows/columns) conditions are given, the specific ones will be used.

Remember, the component operates by first selecting the specified columns and then the specified rows. This order ensures consistency in the extraction process.

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

# Merge Two Dataframes

## General Purpose

The "Merge Two Dataframes" component is designed to combine two tabular datasets into a single dataset. This process is akin to the various types of joins found in SQL, allowing users to merge datasets based on shared keys or indices. This component is essential for situations where you need to integrate data from different sources or when you want to enrich one dataset with additional columns from another.

## Input and Output Format

**Input Format:**
- Two separate dataframes that you wish to merge.

**Output Format:**
- A single dataframe that is the result of merging the two input dataframes.

## Configuration Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| how | String | Type of merge to be performed. Defaults to 'inner'. |
| both_on | String or Tuple | Column name or 'index' to merge on for both dataframes. |
| left_on | String or List | Column name or 'index' to join on in the left dataframe. |
| right_on | String or List | Column name or 'index' to join on in the right dataframe. |
| suffixes | Tuple | Suffixes to apply to overlapping column names. Defaults to ('_0', '_1'). |

## Detailed Configuration Parameters

- **how**: Defines the type of merge to perform. The available options are:
  - 'inner': Merges using the intersection of keys from both frames.
  - 'outer': Merges using the union of keys from both frames.
  - 'left': Merges using only keys from the left frame.
  - 'right': Merges using only keys from the right frame.
  - 'cross': Creates a cartesian product from both frames.

- **both_on**: Specifies the column name or 'index' to merge on for both dataframes. If set to 'index', the index of the dataframe will be used for merging. If a column name is provided, it must be present in both dataframes.

- **left_on**: Indicates the column name or 'index' to join on in the left dataframe. If set to 'index', the index of the dataframe will be used for joining. If a column name is provided, it must be present in the left dataframe.

- **right_on**: Specifies the column name or 'index' to join on in the right dataframe. If set to 'index', the index of the dataframe will be used for joining. If a column name is provided, it must be present in the right dataframe.

- **suffixes**: A tuple of suffixes to apply to overlapping column names in the left and right dataframes to distinguish them after the merge. The default is ('_0', '_1').

## Notes

- If both 'both_on' and 'left_on/right_on' are specified, 'both_on' will be ignored.
- Dataframes are merged iteratively from left to right.
- If using 'left_on' column, all dataframes except the last one should have the column.
- If using 'right_on' column, all dataframes except the first one should have the column.

# Download Component

## General Purpose

The Download Component is designed to facilitate the downloading of files from the internet. It is a pre-built pipeline component that takes a list of URLs and downloads the corresponding files to a specified location within the application's directory structure.

## Input Format

The input for this component is a dataframe containing a single column:

- `link`: This column should contain the URLs of the files that need to be downloaded.

## Output Format

The output of this component is a dataframe with a single column:

- `file`: This column will contain the local file paths to the downloaded files.

## Configuration Parameters

| Parameter | Type   | Description                                                  |
|-----------|--------|--------------------------------------------------------------|
| prefix    | String | (Optional) A prefix to add to the paths of downloaded files. |

## Configuration Parameters Details

- **prefix**: This is an optional configuration parameter. If provided, it will be used as a prefix for the downloaded file paths. This allows the files to be organized in a subdirectory within the app directory. If not specified, files will be downloaded directly to the root of the app directory. It is important to ensure that the prefix does not lead to any conflicts or issues with the file system.

Please note that the configuration parameters should be set in the context of the application before running the component. If there are any errors or issues with the specified prefix, the component will raise an exception and suggest using a different prefix.

# Add Column

## General Purpose

The "Add Column" component is designed to enhance your tabular data by inserting a new column with a constant value. This can be particularly useful when you need to add metadata, flags, or any other consistent information to your dataset.

## Input and Output Format

### Input Format

The input for this component is an arbitrary dataframe that contains the data you wish to modify, along with context information.

### Output Format

The output is the input dataframe with the new column inserted at the specified position.

## Configuration Parameters

| Parameter | Type   | Description                                                                 |
|-----------|--------|-----------------------------------------------------------------------------|
| column    | String | The name of the new column to add.                                          |
| value     | Any    | The constant value to be assigned to all cells in the new column.           |
| position  | Integer| The position at which the new column should be inserted into the dataframe. |

## Configuration Parameters Details

- **column**: This is an optional parameter. If not specified, the default column name used will be 'new_column'. This is the name that will appear as the header for the new column in your dataframe.

- **value**: Also an optional parameter, with a default value of 'new_value'. This value will be assigned to every cell in the new column, effectively creating a constant column.

- **position**: This integer parameter is optional and defaults to 0, meaning the new column will be inserted at the beginning of the dataframe by default. If a positive value is provided, the new column will be inserted at that position, counting from the beginning. If a negative value is provided, the column will be inserted from the end of the dataframe. For example, a position of -1 will place the new column as the last column.

# Rename Columns

## General Component Purpose

The "Rename Columns" component is designed to change the names of columns within a tabular dataset. This operation is useful when you want to standardize column names, correct typos, or make the names more descriptive for further data processing and analysis.

## Input and Output Format

### Input Format

- **DataFrame**: The input is a DataFrame that contains the columns which need to be renamed.

### Output Format

- **DataFrame**: The output is a DataFrame with the same data as the input, but with the column names changed according to the configuration provided.

## Configuration Parameters

| Parameter Name | Expected Type       | Description                                       |
|----------------|---------------------|---------------------------------------------------|
| column_mapping | Dictionary of Strings | A mapping of old column names to their new names. |

## Configuration Parameters Details

- **column_mapping**: This is a dictionary where each key-value pair represents a column name change. The key is the original column name, and the value is the new column name that will replace it. For example, to rename the columns 'a', 'b', 'c' to 'A', 'B', 'C', respectively, the configuration should be:

```json
{
    "a": "A",
    "b": "B",
    "c": "C"
}
```

This configuration will instruct the component to look for columns named 'a', 'b', and 'c' in the input DataFrame and rename them to 'A', 'B', and 'C', respectively.

The "Rename Columns" component simplifies the process of altering column names in a dataset, making it an essential tool for data preparation and cleaning. It ensures that the data conforms to a desired naming convention without the need for manual intervention or coding.

# Squash Component

## General Purpose

The Squash component is designed to transform tabular data by condensing multiple rows into a single row. This process is particularly useful when you want to aggregate data that shares a common value in a specific column. The result is a more compact representation of the original data, which can be beneficial for summary views or when preparing data for further analysis.

## Input and Output Format

**Input Format:** The component accepts any arbitrary dataframe with columns that contain multiple values.

**Output Format:** The output is a dataframe with the same columns as the input dataframe. However, the output dataframe has multiple rows for each input row squashed into a single row, based on the specified configuration.

## Configuration Parameters

| Name   | Type   | Description |
|--------|--------|-------------|
| by     | String | The column to group by. If not specified, all columns will be squashed. |
| delim  | String | The delimiter used to separate values in the columns. The default delimiter is a comma (,). |

## Configuration Parameters Details

- **by**: This parameter specifies the column name based on which the squashing of rows will occur. If this parameter is not provided, the squashing will be applied across all columns.

- **delim**: This parameter defines the character or string that will be used to separate the values in the squashed row. By default, if this parameter is not specified, a comma (`,`) will be used as the delimiter.

# Merge DataFrames Component

## General Purpose

The Merge DataFrames component is designed to combine multiple tabular datasets into a single dataset. This is analogous to performing SQL-style joins where datasets can be merged based on common keys or indices. It is a versatile component that supports various types of merges, such as inner, outer, left, right, and cross joins. This allows for flexibility in how datasets are combined, depending on the specific requirements of the product pipeline.

## Input and Output Format

- **Input**: An iterable containing multiple dataframes to be merged.
- **Output**: A single dataframe that is the result of merging the input dataframes according to the specified configuration.

## Configuration Parameters

| Parameter Name | Expected Type          | Description                                                   |
|----------------|------------------------|---------------------------------------------------------------|
| how            | String                 | The type of merge to be performed (inner, outer, left, right, cross). |
| both_on        | String or Tuple        | Column name or 'index' to merge on for both dataframes.       |
| left_on        | String or List of Strings | Column name or 'index' to join on in the left DataFrame.     |
| right_on       | String or List of Strings | Column name or 'index' to join on in the right DataFrame.    |
| suffixes       | Tuple                  | Suffixes to apply to overlapping column names.                |

## Detailed Configuration Parameters

- **how**: Defines the type of merge to be performed. The default is 'inner'. Possible values include:
  - 'inner': Only the common keys from both frames are used.
  - 'outer': All keys from both frames are used.
  - 'left': Only keys from the left frame are used.
  - 'right': Only keys from the right frame are used.
  - 'cross': A cartesian product of both frames is created.

- **both_on**: Specifies the column name or 'index' to merge on for both dataframes. If the value is 'index', the index of the dataframe will be used for merging. If a column name is provided, it must be present in all dataframes.

- **left_on**: Indicates the column name or 'index' to join on in the left DataFrame. If the value is 'index', the index of the dataframe will be used for joining. If a column name is provided, it must be present in all but the last dataframe.

- **right_on**: Specifies the column name or 'index' to join on in the right DataFrame. If the value is 'index', the index of the dataframe will be used for joining. If a column name is provided, it must be present in all but the first dataframe.

- **suffixes**: A tuple that defines the suffixes to apply to overlapping column names in the left and right dataframes. The default is ('_0', '_1').

## Notes

- If both 'both_on' and 'left_on/right_on' are provided, 'both_on' will be ignored.
- Dataframes are merged iteratively from left to right.
- If using 'left_on' column, all dataframes except the last one should have the column.
- If using 'right_on' column, all dataframes except the first one should have the column.

By configuring the component correctly, users can easily merge multiple datasets into a single dataset that can be used for further analysis or processing within the product pipeline.

# Merge Three Dataframes

## General Purpose

The "Merge Three Dataframes" component is designed to combine three separate tabular datasets into a single dataset. This process is similar to the join operations in SQL and is essential for integrating data that originates from different sources but shares common keys or indices.

## Input and Output Format

### Input Format
The component accepts three input dataframes, each containing tabular data.

### Output Format
The output is a single dataframe that represents the merged result of the three input dataframes.

## Configuration Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| how       | String | The type of merge to be performed. Defaults to 'inner'. |
| both_on   | String or Tuple | The key(s) on which to merge the dataframes. Can be a column name or 'index'. |
| left_on   | String or List of Strings | The key(s) for the left dataframe to join on. Can be a column name or 'index'. |
| right_on  | String or List of Strings | The key(s) for the right dataframe to join on. Can be a column name or 'index'. |
| suffixes  | Tuple | Suffixes to apply to overlapping column names. Defaults to ('_0', '_1'). |

## Detailed Configuration Parameters

- **how**: Specifies the type of merge operation. Possible values are:
  - 'inner': Keeps only rows that match in both dataframes.
  - 'outer': Keeps all rows from both dataframes, filling in NaNs for missing matches.
  - 'left': Keeps all rows from the left dataframe and matching rows from the right dataframe.
  - 'right': Keeps all rows from the right dataframe and matching rows from the left dataframe.
  - 'cross': Creates a cartesian product of rows from both dataframes.

- **both_on**: If provided, this parameter is used as the merge key for all three dataframes. If set to 'index', the dataframes' indices are used as the merge key. If a column name is provided, it must be present in all dataframes.

- **left_on**: This parameter specifies the merge key for the left dataframe. If set to 'index', the left dataframe's index is used. If a column name is provided, it must be present in all dataframes except the last one.

- **right_on**: This parameter specifies the merge key for the right dataframe. If set to 'index', the right dataframe's index is used. If a column name is provided, it must be present in all dataframes except the first one.

- **suffixes**: When column names overlap, these suffixes are appended to the columns from the left and right dataframes to differentiate them. The default is ('_0', '_1').

## Notes

- If both 'both_on' and 'left_on/right_on' are specified, 'both_on' will take precedence and be used for the merge.
- The dataframes are merged in sequence, starting with the leftmost dataframe and moving to the right.
- When using 'left_on', ensure that the specified column is present in all dataframes except the last one.
- When using 'right_on', ensure that the specified column is present in all dataframes except the first one.

