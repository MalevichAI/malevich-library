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
                    issue{{
                        id
                    }}
                }}
            }}
            """)
        response = self.client.execute(doc)
        return response['issueCreate']['issue']['id']

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
        response = self.client.execute(doc)
        return response['issueUpdate']['success']

    def get_issues(self, team_key: str):
        doc = gql(
            f"""
                query{{
                    issues(
                        filter:{{
                            team:{{
                                key: {{
                                    eq: "{team_key}"
                                }}
                            }}
                        }}){{
                        nodes {{
                            id
                            title
                            description
                            priority
                            state {{
                                name
                            }}
                            assignee {{
                                name
                                email
                            }}
                        }}
                    }}
                }}
            """
        )
        response = self.client.execute(doc)
        return response['issues']['nodes']

    def get_users_in_team(self, team_key):
        doc = gql(
            f"""
            query{{
               teams(
                filter:{{
                    key:{{
                    eq: "{team_key}"
                    }}
                }}){{
                nodes {{
                    members {{
                    nodes {{
                        name
                        email
                    }}
                    }}
                }}
                }}
            }}
            """
        )
        response = self.client.execute(doc)
        return response['teams']['nodes'][0]['members']['nodes']

    def get_projects(self, team_key):
        doc = gql(
           f"""
            query{{
                projects(
                    filter:{{
                        accessibleTeams:{{
                            some: {{
                                key:{{
                                    eq: "{team_key}"
                                }}
                            }}
                        }}
                    }}){{
                    nodes {{
                        id
                        name
                        members {{
                            nodes {{
                            name
                            email
                            }}
                        }}
                    }}
                }}
            }}
            """
        )
        response = self.client.execute(doc)
        return response['projects']['nodes']

    def get_project_by_identifier(self, project_id):
        doc = gql(
            f"""
            query ExampleQuery {{
                project(
                    id: "{project_id}"
                ){{
                    name
                }}
                }}
            """
        )
        response = self.client.execute(doc)
        return response['project']['name']
