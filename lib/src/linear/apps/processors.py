"""
Author: Leonid Zelenskiy
"""


import pandas as pd
from malevich.square import DF, Context, processor, scheme
from pydantic import BaseModel

from .linear import LinearExecutor


@scheme()
class GetProjectInputSchema(BaseModel):
    project_id: str


@scheme()
class CreateIssueSchema(BaseModel):
    title: str
    description: str
    team_key: str
    project_name: str
    priority: int
    state: str


@scheme()
class AssignUserSchema(BaseModel):
    title: str
    email: str


@scheme()
class GetObjects(BaseModel):
    team_key: str


@processor()
def get_project(df: DF[GetProjectInputSchema], context: Context):
    """Get project by identifier

    Input:
        A dataframe with a column named `project_id` containing project id.

    Output:
        A dataframe with a column named `project` containing project.

    Args:
        df (DF[GetProjectInputSchema]):
            A dataframe with a column named `project_id` containing project id.

    Returns:
        DF[Project]:
            A dataframe with a column named `project` containing project.
    """
    linear: LinearExecutor = context.common
    outputs = []
    for _, row in df.iterrows():
        outputs.append(linear.get_project_by_identifier(row['project_id']))
    return pd.DataFrame(outputs, columns=['project_name'])


@processor()
def create_issue(df: DF[CreateIssueSchema], context: Context):
    """
    Create issue and assign to user

    Input:
        A dataframe with columns:
            title: Title of the Issue
            description: Description of the Issue
            team_key: Team key, for example 'ABC'
            project_name: Name of the project
            priority:
                Priority from 0 to 4
                (0 = No priority, 1 = Urgent, 2 = High, 3 = Normal, 4 = Low.)
            state: State of the Issue

    Output:
        A dataframe with a column named `issue_id` containing issue ids.

    Args:
        df (DF[GetProjectInputSchema]):
            A dataframe with issue inputs.

    Returns:
        DF[Issue]:
            A dataframe with a column named `issue_id` containing issue ids.
    """  # noqa: E501
    linear: LinearExecutor = context.common
    outputs = []
    for _, row in df.iterrows():
        outputs.append(
            linear.create_issue(
                row['title'],
                row['description'],
                row['team_key'],
                row['project_name'],
                row['priority'],
                row['state']
            )
        )
    return pd.DataFrame(outputs, columns=['issue_id'])


@processor()
def assign_user(df: DF[AssignUserSchema], context: Context):
    """
    Assign user to the issue

    Input:
        A dataframe with columns:
            title: Title of an issue
            email: Asignee email

    Output:
        A dataframe with columns:
            title: Issue title
            email: Assignee email
            success: Was it success or not

    Args:
        df (DF[GetProjectInputSchema]):
            A dataframe with Assigning inputs.

    Returns:
        DF[AssignSuccess]:
            A dataframe with columns:
                title: Issue title
                email: Assignee email
                success: Was it success or not
    """  # noqa: E501
    linear: LinearExecutor = context.common
    outputs = []
    for _, row in df.iterrows():
        outputs.append(
            str(
                linear.assign_user(row['email'], row['title'])
            )
        )
    df.insert(2, 'success', outputs)
    return df


@processor()
def get_issues(df: DF[GetObjects], context: Context):
    """
    Get all issues in the team

    Input:
        A dataframe with a column named 'team_key' containing team key (example 'ABC')

    Output:
        A dataframe with columns:
            team_key: Team Key
            id: Issue id
            title: Issue title
            description: Issue description
            priority: Issue priority from 0 to 4 (0 = No priority, 1 = Urgent, 2 = High, 3 = Normal, 4 = Low.)
            state: Issue state
            assignee_name: Assignee name
            assignee_email: Assignee email

    Args:
        df (DF[GetObjects]):
            A dataframe with a column named 'team_key' containing team key

    Returns:
        Dataframe information about issues
    """   # noqa: E501
    linear: LinearExecutor = context.common
    data = {
        "team_key": [],
        "id": [],
        "title": [],
        "description": [],
        "priority": [],
        "state": [],
        "assignee_name": [],
        "assignee_email": []
    }
    for _, row in df.iterrows():
        issues = linear.get_issues(row['team_key'])
        for issue in issues:
            data['team_key'].append(row['team_key'])
            data['id'].append(issue['id'])
            data["title"].append(issue['title'])
            data["description"].append(issue['description'])
            data["priority"].append(issue['priority'])
            data["state"].append(issue['state']['name'])
            data["assignee_name"].append(
                'Empty' if issue['assignee'] is None
                else issue['assignee']['name']
            )
            data["assignee_email"].append(
                'Empty' if issue['assignee'] is None
                else issue['assignee']['email']
            )

    return pd.DataFrame(
        data=data
    )


@processor()
def get_projects(df: DF[GetObjects], context: Context):
    """
    Get all projects in the team

    Input:
        A dataframe with a column named 'team_key' containing team key (example 'ABC')

    Output:
        A dataframe with columns:
            team_key: Team Key
            project_id: ID of the project
            project_name: Name of the project
            member_name: Name of project member
            member_email: Email of project member

    Args:
        df (DF[GetObjects]):
            A dataframe with a column named 'team_key' containing team key

    Returns:
        DF[Project]:
            team_key: Team Key
            project_id: ID of the project
            project_name: Name of the project
            member_name: Name of project member
            member_email: Email of project member
    """
    linear: LinearExecutor = context.common
    outputs = []
    for _, row in df.iterrows():
        data = linear.get_projects(row['team_key'])
        for node in data:
            for mem in node['members']['nodes']:
                outputs.append([
                    row['team_key'],
                    node['id'],
                    node['name'],
                    mem['name'],
                    mem['email']
                ])
    return pd.DataFrame(
        outputs,
        columns=[
            'team_key',
            'project_id',
            'project_name',
            'member_name',
            'member_email'
        ]
    )


@processor()
def get_users(df: DF[GetObjects], context: Context):
    """
        Get all users in the team

        Input:
            A dataframe with a column named 'team_key' containing team key (example 'ABC')

        Output:
            A dataframe with columns:
                team_key: Team key, for example 'ABC'
                name: Name of user
                email: Email of user

        Args:
            df (DF[GetObjects]):
                A dataframe with a column named 'team_key' containing team key

        Returns:
            DF[User]:
                team_key: Team key, for example 'ABC'
                name: Name of user
                email: Email of user
    """  # noqa: E501
    linear: LinearExecutor = context.common
    outputs = []

    for _, row in df.iterrows():
        users = linear.get_users_in_team(row['team_key'])
        for user in users:
            outputs.append([row['team_key'], user['name'], user['email']])

    return pd.DataFrame(outputs, columns=['team_key', 'name', 'email'])
