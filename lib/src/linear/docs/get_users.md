# Get Users

## General Purpose

The "Get Users" component is designed to retrieve all users within a specific team. It is useful for gathering information about team members, including their names and email addresses. This component can be used in scenarios where team collaboration and communication are essential, and there is a need to obtain a list of all team members for further processing or contact.

## Input Format

The input for this component is a dataframe with a single column:

- `team_key`: A column containing the team key (e.g., 'ABC') which is used to identify the team whose users are to be retrieved.

## Output Format

The output is a dataframe with the following columns:

- `team_key`: The team key, corresponding to the input team key.
- `name`: The name of the user.
- `email`: The email address of the user.

## Configuration Parameters

There are no additional configuration parameters for this component. It uses the `team_key` from the input dataframe to perform its operation.

## Detailed Parameter Descriptions

Since this component does not require any extra configuration parameters, you only need to ensure that the input dataframe contains the correct `team_key` column to use the "Get Users" component effectively. The component will automatically handle the retrieval and organization of user information based on the provided team keys.