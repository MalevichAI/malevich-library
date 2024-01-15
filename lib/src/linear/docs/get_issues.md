# Get Issues Component

## General Purpose

The "Get Issues" component is designed to retrieve information about issues within a team. It processes a given dataset to extract details about each issue, such as the issue ID, title, description, priority, state, and assignee information. This component is useful for generating comprehensive reports on team issues or for integrating issue data into other product pipelines.

## Input and Output Format

### Input Format

The input for this component is a dataframe that must contain the following column:

- `team_key`: A string representing the team key (e.g., 'ABC').

### Output Format

The output is a dataframe with the following columns:

- `team_key`: Team Key
- `id`: Issue ID
- `title`: Issue Title
- `description`: Issue Description
- `priority`: Issue Priority (ranging from 0 to 4, where 0 = No priority, 1 = Urgent, 2 = High, 3 = Normal, 4 = Low)
- `state`: Issue State
- `assignee_name`: Assignee Name (marked as 'Empty' if no assignee)
- `assignee_email`: Assignee Email (marked as 'Empty' if no assignee)

## Configuration Parameters

No additional configuration parameters are required for this component.

## Detailed Parameter Descriptions

Since there are no additional configuration parameters for this component, you only need to ensure that the input dataframe contains the required `team_key` column. The component will handle the retrieval and structuring of issue data automatically.

For any further assistance or clarification on using the "Get Issues" component, please contact our support team.