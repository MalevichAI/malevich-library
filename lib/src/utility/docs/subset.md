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