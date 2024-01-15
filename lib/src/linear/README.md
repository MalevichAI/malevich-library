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

# Get Projects

## General Component Purpose
The "Get Projects" component is designed to retrieve all projects within a specified team. It takes the team's key as input and outputs a list of projects, including details about each project and its members.

## Input Format
The input for this component is a dataframe that must contain the following column:

- `team_key`: A column containing the team key (e.g., 'ABC').

## Output Format
The output is a dataframe with the following columns:

- `team_key`: The team key associated with the projects.
- `project_id`: The unique identifier for each project.
- `project_name`: The name of each project.
- `member_name`: The name of each member associated with the project.
- `member_email`: The email address of each project member.

## Configuration Parameters

| Parameter Name | Expected Type   | Description                              |
|----------------|-----------------|------------------------------------------|
| df             | DataFrame       | Dataframe with the 'team_key' column.    |

## Configuration Parameters Details

- **df (DataFrame)**: This is the input dataframe that must include a 'team_key' column. The 'team_key' is used to identify the team and retrieve all associated projects and their member details.

Please ensure that the input dataframe is correctly formatted with the required column to avoid any errors during the component execution. The output will provide a comprehensive list of projects and their members, which can be used for further analysis or reporting within your organization.

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

