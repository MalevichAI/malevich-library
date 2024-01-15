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