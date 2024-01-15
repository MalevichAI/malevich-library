# Assign User to Issue

## General Purpose
The "Assign User to Issue" component is designed to automate the process of assigning a user to an issue within a project management context. It takes in a list of issues and the corresponding assignee emails and updates each issue with the assignment status.

## Input Format
The input for this component is a tabular data format with the following columns:

- **title**: Title of an issue.
- **email**: Assignee's email address.

## Output Format
The output is a table that includes the original data plus an additional column:

- **title**: Issue title.
- **email**: Assignee email.
- **success**: Indicates whether the assignment was successful or not.

## Configuration Parameters

| Parameter Name | Expected Type | Description |
| -------------- | ------------- | ----------- |
| `df`           | Dataframe     | A dataframe containing the issues to be assigned along with the assignee emails. |

## Detailed Parameter Descriptions

- **df (Dataframe)**: This is the primary input to the component, which should adhere to the specified input format. It contains the information about the issues and the corresponding assignees. The dataframe is expected to have columns for the issue title and the assignee's email address.

The component utilizes an internal mechanism to perform the assignment and will output the result in a new column indicating the success of each operation. This allows users to quickly identify any issues that could not be assigned and take appropriate action.