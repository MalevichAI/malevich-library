# Add Column

## General Purpose

The "Add Column" component is designed to enhance your tabular data by inserting a new column with a constant value. This can be particularly useful when you need to add metadata, flags, or any other consistent information to your dataset.

## Input and Output Format

### Input Format

The input for this component is an arbitrary dataframe that contains the data you wish to modify, along with context information.

### Output Format

The output is the input dataframe with the new column inserted at the specified position.

## Configuration Parameters

| Parameter | Type   | Description                                                                 |
|-----------|--------|-----------------------------------------------------------------------------|
| column    | String | The name of the new column to add.                                          |
| value     | Any    | The constant value to be assigned to all cells in the new column.           |
| position  | Integer| The position at which the new column should be inserted into the dataframe. |

## Configuration Parameters Details

- **column**: This is an optional parameter. If not specified, the default column name used will be 'new_column'. This is the name that will appear as the header for the new column in your dataframe.

- **value**: Also an optional parameter, with a default value of 'new_value'. This value will be assigned to every cell in the new column, effectively creating a constant column.

- **position**: This integer parameter is optional and defaults to 0, meaning the new column will be inserted at the beginning of the dataframe by default. If a positive value is provided, the new column will be inserted at that position, counting from the beginning. If a negative value is provided, the column will be inserted from the end of the dataframe. For example, a position of -1 will place the new column as the last column.