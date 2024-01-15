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