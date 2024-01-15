# Filter Component

## General Purpose

The Filter Component is designed to refine and reduce the data in a tabular format based on specified conditions. It allows users to apply various filtering operations to select only the rows that meet certain criteria. This component is essential for data preprocessing, enabling users to focus on relevant data and exclude the unnecessary or irrelevant entries.

## Input and Output Format

**Input Format**: The input for the Filter Component is an arbitrary dataframe that you wish to filter.

**Output Format**: The output is a dataframe that contains only the rows that meet the specified filtering conditions.

## Configuration Parameters

| Name       | Expected Type      | Description                                           |
|------------|--------------------|-------------------------------------------------------|
| conditions | List of Dictionaries | A list of conditions that specify the filtering criteria. |

## Configuration Parameters Details

- **conditions**: This is a list where each item is a dictionary that defines a single filtering condition. Each dictionary can have the following keys:
  - **column**: The name of the column in the dataframe to apply the filter on.
  - **operation**: The operation to use for filtering (e.g., 'equal', 'greater', 'less', 'like', etc.).
  - **value**: The value to compare against when filtering.
  - **type** (optional): The data type of the value (e.g., 'int', 'float', 'bool', 'str'). If not specified, 'str' is assumed.

### Supported Operations

- **equal**: Select rows where the column value is equal to the specified value.
- **not_equal**: Select rows where the column value is not equal to the specified value.
- **greater**: Select rows where the column value is greater than the specified value.
- **greater_equal**: Select rows where the column value is greater than or equal to the specified value.
- **less**: Select rows where the column value is less than the specified value.
- **less_equal**: Select rows where the column value is less than or equal to the specified value.
- **in**: Select rows where the column value is in a list of specified values.
- **not_in**: Select rows where the column value is not in a list of specified values.
- **like**: Select rows where the column value contains the specified substring.
- **not_like**: Select rows where the column value does not contain the specified substring.
- **is_null**: Select rows where the column value is null.
- **is_not_null**: Select rows where the column value is not null.

### Supported Types

- **int**: Integer type.
- **float**: Floating point number type.
- **bool**: Boolean type.
- **str**: String type.

The Filter Component is a powerful tool for data manipulation, allowing users to easily refine their datasets without writing any code. By configuring the conditions appropriately, users can create complex filters to process their data efficiently.