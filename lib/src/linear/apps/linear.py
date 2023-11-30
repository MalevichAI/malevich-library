from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport


class LinearExecutor:

    def __init__(self, url: str, headers: dict) -> None:
        self.client = Client(transport=RequestsHTTPTransport(url, headers=headers))

    def get_team_id(self, team_key: str):
        doc = gql(
            f'''
            query{{
                teams(filter: {{
                    key: {{
                    eq: "{team_key}"
                    }}
                }}) {{
                    nodes {{
                    id
                    }}
                }}
                }}
            ''')
        result = self.client.execute(doc)
        return result['teams']['nodes'][0]['id']

    def get_project_id(self, project_name: str):
        doc = gql(
            f'''
            query{{
                projects(filter: {{
                    name: {{
                    eq: "{project_name}"
                    }}
                }}) {{
                    nodes {{
                    id
                    }}
                }}
                }}
            ''')
        result = self.client.execute(doc)
        return result['projects']['nodes'][0]['id']

    def get_state_id(self, team_key, state):
        doc = gql(
            f"""
            query{{
                workflowStates(
                filter: {{
                    team: {{
                    key: {{
                    eq: "{team_key}"
                    }}
                    }}
                    name: {{
                    eq: "{state}"
                    }}
                }}
                ){{
                nodes {{
                    id
                }}
                }}
            }}
            """
        )
        result = self.client.execute(doc)
        return result['workflowStates']['nodes'][0]['id']

    def get_user_id(self, email):
        doc = gql(
            f"""
                query{{
                    users(filter: {{
                        email: {{
                            eq: "{email}"
                        }}
                    }}) {{
                        nodes{{
                        id
                        }}
                    }}
                    }}
            """
        )
        result = self.client.execute(doc)
        return result['users']['nodes'][0]['id']

    def get_issue_id(self, title):
        doc = gql(
            f"""
            query{{
                issues(filter: {{
                    title: {{
                    eq: "{title}"
                    }}
                }}) {{
                    nodes {{
                        id
                        }}
                }}
                }}
            """
        )
        response = self.client.execute(doc)
        return response['issues']['nodes'][0]['id']

    def create_issue(
                    self,
                    title: str,
                    description: str,
                    team_key: str,
                    project_name: str,
                    priority: int,
                    state: str,
                    email: str|None=None
                ):
        team_id = self.get_team_id(team_key)
        project_id = self.get_project_id(project_name)
        state_id = self.get_state_id(team_key, state)
        doc = gql(
            f"""
            mutation{{
                issueCreate(
                    input:{{
                        title: "{title}"
                        description: "{description}"
                        teamId: "{team_id}"
                        projectId: "{project_id}"
                        priority: {priority}
                        stateId: "{state_id}"
                    }}
                ){{
                    success
                }}
            }}
            """)
        response = self.client.execute(doc)
        print(response)
        if email is not None:
            self.assign_user(email, title)

    def assign_user(self, email, title):
        user_id = self.get_user_id(email)
        issue_id = self.get_issue_id(title)
        doc = gql(
            f"""
                mutation{{
                    issueUpdate(
                        input:{{
                            assigneeId: "{user_id}"
                        }},
                        id: "{issue_id}"
                    ){{
                        success
                    }}
                    }}
            """
        )
        self.client.execute(doc)


    def get_issues(self):
        doc = gql(
            """
                query{
                    issues {
                        nodes {
                            id
                            title
                            description
                            priority
                            state {
                                name
                            }
                            assignee {
                                name
                                email
                            }
                        }
                    }
                }
            """
        )
        response = self.client.execute(doc)
        return response['issues']['nodes']

    def get_users(self):
        doc = gql(
            """
            query{
                users{
                    nodes {
                        id
                        name
                        email
                    }
                }
            }
            """
        )
        response = self.client.execute(doc)
        return response['users']['nodes']

    def get_teams(self):
        doc = gql(
            """
            query{
                teams{
                    nodes {
                        id
                        key
                        name
                        description
                        members {
                            nodes {
                            name
                            email
                            }
                        }
                    }
                }
            }
            """
        )
        response = self.client.execute(doc)
        return response['teams']['nodes']

    def get_projects(self):
        doc = gql(
            """
            query{
                projects{
                    nodes {
                        id
                        name
                        members {
                            nodes {
                            name
                            email
                            }
                        }
                    }
                }
            }
            """
        )
        response = self.client.execute(doc)
        return response['projects']['nodes']


if __name__ == '__main__':
    headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Linear API Key'
        }
    client = LinearExecutor('https://api.linear.app/graphql', headers)
