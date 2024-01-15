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