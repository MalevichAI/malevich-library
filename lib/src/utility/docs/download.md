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