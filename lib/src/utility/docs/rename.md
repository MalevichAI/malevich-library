# Rename Columns

## General Component Purpose

The "Rename Columns" component is designed to change the names of columns within a tabular dataset. This operation is useful when you want to standardize column names, correct typos, or make the names more descriptive for further data processing and analysis.

## Input and Output Format

### Input Format

- **DataFrame**: The input is a DataFrame that contains the columns which need to be renamed.

### Output Format

- **DataFrame**: The output is a DataFrame with the same data as the input, but with the column names changed according to the configuration provided.

## Configuration Parameters

| Parameter Name | Expected Type       | Description                                       |
|----------------|---------------------|---------------------------------------------------|
| column_mapping | Dictionary of Strings | A mapping of old column names to their new names. |

## Configuration Parameters Details

- **column_mapping**: This is a dictionary where each key-value pair represents a column name change. The key is the original column name, and the value is the new column name that will replace it. For example, to rename the columns 'a', 'b', 'c' to 'A', 'B', 'C', respectively, the configuration should be:

```json
{
    "a": "A",
    "b": "B",
    "c": "C"
}
```

This configuration will instruct the component to look for columns named 'a', 'b', and 'c' in the input DataFrame and rename them to 'A', 'B', and 'C', respectively.

The "Rename Columns" component simplifies the process of altering column names in a dataset, making it an essential tool for data preparation and cleaning. It ensures that the data conforms to a desired naming convention without the need for manual intervention or coding.