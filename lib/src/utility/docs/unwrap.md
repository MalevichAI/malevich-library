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