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