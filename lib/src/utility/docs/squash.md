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