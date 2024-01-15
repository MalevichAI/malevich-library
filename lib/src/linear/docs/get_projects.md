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