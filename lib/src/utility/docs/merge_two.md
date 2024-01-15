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