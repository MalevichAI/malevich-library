# Create Issue and Assign to User

## General Purpose

The "Create Issue and Assign to User" component is designed to automate the process of creating issues within a project management system and assigning them to the appropriate team. It takes in tabular data representing the details of the issues to be created, including titles, descriptions, team keys, project names, priorities, and states. The component then processes this information and generates a new table containing the unique identifiers (issue IDs) for the newly created issues.

## Input Format

The input for this component is a dataframe with the following columns:

- `title`: The title of the issue.
- `description`: A detailed description of the issue.
- `team_key`: The key identifier for the team, e.g., 'ABC'.
- `project_name`: The name of the project where the issue will be created.
- `priority`: The priority level of the issue, ranging from 0 to 4 (0 = No priority, 1 = Urgent, 2 = High, 3 = Normal, 4 = Low).
- `state`: The current state of the issue.

## Output Format

The output is a dataframe with a single column:

- `issue_id`: The unique identifier for each created issue.

## Configuration Parameters

| Parameter Name | Expected Type       | Description                                      |
| -------------- | ------------------- | ------------------------------------------------ |
| title          | String              | The title of the issue.                           |
| description    | String              | A detailed description of the issue.             |
| team_key       | String              | The team key, e.g., 'ABC'.                       |
| project_name   | String              | The name of the project.                         |
| priority       | Integer (0 to 4)    | The priority level of the issue.                 |
| state          | String              | The current state of the issue.                  |

## Detailed Parameter Descriptions

- **title**: This is a brief, descriptive title for the issue. It should be concise yet informative enough to give an overview of the issue at a glance.
  
- **description**: This provides a more in-depth explanation of the issue, potentially including steps to reproduce, expected outcomes, and any other relevant details.
  
- **team_key**: This is an identifier used to assign the issue to the correct team within the organization. It should match the team's key in the project management system.
  
- **project_name**: This is the name of the project under which the issue will be filed. It helps in organizing and categorizing the issues correctly.
  
- **priority**: This integer value represents the urgency of the issue, with 0 being no priority and 4 being the lowest priority. It is used to help teams prioritize their workloads.
  
- **state**: This indicates the current status of the issue, such as 'Open', 'In Progress', or 'Closed'. It helps in tracking the progress of issue resolution.