# Locate Statically Component

## General Purpose

The Locate Statically component is designed to extract specific subsets of data from a larger tabular dataset. It allows users to select particular rows and columns based on their names, indexes, or a combination of both. This component is useful when you need to focus on a certain part of your data for further analysis or processing.

## Input and Output Format

- **Input Format**: The component accepts a tabular dataset, commonly referred to as a DataFrame.
- **Output Format**: The output is a subset of the input DataFrame, containing only the selected rows and columns.

## Configuration Parameters

| Parameter Name | Expected Type       | Description                                           |
| -------------- | ------------------- | ----------------------------------------------------- |
| `column`       | String              | The name of the single column to be extracted.        |
| `columns`      | List of Strings     | The names of multiple columns to be extracted.        |
| `column_idx`   | Integer             | The index of a single column to be extracted.         |
| `column_idxs`  | List of Integers    | The indexes of multiple columns to be extracted.      |
| `row`          | Integer             | The index of a single row to be extracted.            |
| `rows`         | List of Integers    | The indexes of multiple rows to be extracted.         |
| `row_idx`      | Integer             | The index of a single row to be extracted.            |
| `row_idxs`     | List of Integers    | The indexes of multiple rows to be extracted.         |

## Detailed Configuration Parameters

- **`column`**: Specify the name of a single column to extract from the DataFrame. This is useful when you are interested in one specific column.

- **`columns`**: Provide a list of column names if you need to extract multiple columns. This is useful for analyzing or comparing specific features within your dataset.

- **`column_idx`**: Use this parameter to select a column by its index rather than its name. This can be handy when working with unnamed columns or when the name is not known.

- **`column_idxs`**: Similar to `column_idx`, but allows for selection of multiple columns by their indexes.

- **`row`**: This parameter allows you to select a single row from the DataFrame based on its index.

- **`rows`**: If you need to extract multiple rows, provide their indexes in a list. This is useful for extracting specific records.

- **`row_idx`**: Select a single row using its index. This is useful when you need to analyze or manipulate a specific entry in your dataset.

- **`row_idxs`**: A list of row indexes to extract multiple rows at once.

Please note that at least one of the above configuration parameters must be provided for the component to function properly. The extraction process prioritizes specificity; if both specific (single row/column) and general (multiple rows/columns) conditions are given, the specific ones will be used.

Remember, the component operates by first selecting the specified columns and then the specified rows. This order ensures consistency in the extraction process.