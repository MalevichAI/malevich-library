# Get Project

## General Purpose

The "Get Project" component is designed to transform tabular data by retrieving project information based on provided project identifiers. It is a crucial component for users who need to enrich their data with project details without writing any code.

## Input Format

The input for this component is a dataframe that must contain a single column:

- `project_id`: The column containing unique project identifiers.

## Output Format

The output is a dataframe with the following column:

- `project`: The column containing the retrieved project information corresponding to each `project_id`.

## Configuration Parameters

| Parameter Name | Expected Type | Description |
| -------------- | ------------- | ----------- |
| `project_id`   | String        | The unique identifier for a project to be retrieved. |

## Detailed Parameter Descriptions

- **`project_id`**: This is a unique identifier used to fetch the corresponding project details. It should be provided in the input dataframe, and the component will output the project information associated with each identifier in the output dataframe. 

This component leverages the capabilities of the Malevich package to process the data efficiently and requires no coding experience from the user. It is optimized for performance, ensuring a seamless and fast experience when integrating into product pipelines.