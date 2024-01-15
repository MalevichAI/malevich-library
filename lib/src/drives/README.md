# Download from Google Drive

## General Purpose

The "Download from Google Drive" component is designed to facilitate the downloading of files from Google Drive links provided in a tabular format. It is a convenient tool for users who need to retrieve files from Google Drive and make them available for further processing within the platform.

## Input Format

The input for this component is a dataframe that must contain a column named `link`. Each row in this column should contain a single Google Drive link from which a file will be downloaded.

## Output Format

The output is a dataframe with a column named `filename`. This column contains the names of the files that have been successfully downloaded from the provided Google Drive links.

## Configuration Parameters

| Parameter Name | Expected Type | Description |
| -------------- | ------------- | ----------- |
| fail_on_error  | Boolean       | Determines whether the process should fail upon encountering an error with any of the links. |

## Configuration Parameters Details

- **fail_on_error**: This parameter accepts a Boolean value (`True` or `False`). The default value is `False`. If set to `True`, the component will halt and raise an error if it encounters any invalid links during the download process. If `False`, the component will attempt to continue with the next available link, logging any errors encountered without stopping the entire process.

