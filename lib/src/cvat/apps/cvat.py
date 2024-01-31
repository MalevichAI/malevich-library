import json

import boto3
import pandas as pd
import requests
from malevich.square import DF, Context, processor, scheme
from pydantic import BaseModel
from requests.auth import HTTPBasicAuth


@scheme()
class TaskImages(BaseModel):
    task: str
    image: str

@processor()
def upload_images_to_task(df: DF[TaskImages], context: Context):
    """
        Create task (if does not exists) and upload images to the task

        Configuration:
        cvat_user, cvat_password - CVAT account credentials
        cvat_url - URL of your CVAT server
        aws_access_key_id, aws_secret_access_key - AWS user credentials
        endpoint_url - In case if you do not use default AWS S3, provide endpoint URL

        cloud_storage_id - ID of CVAT cloud storage
        project_id - ID of CVAT project

    """
    login = context.app_cfg.get('cvat_user', None)
    password = context.app_cfg.get('cvat_password', None)
    assert login and password, "CVAT credentials were not provided"

    cvat_url = context.app_cfg.get('cvat_url', None)
    assert cvat_url, "CVAT link was not provided"

    key_id = context.app_cfg.get('aws_access_key_id', None)
    secret_key = context.app_cfg.get('aws_secret_access_key', None)
    assert key_id and secret_key, "AWS credentials were not provided"

    endpoint_url = context.app_cfg.get('endpoint_url', None)
    bucket_name = context.app_cfg.get('bucket_name', 'cvat')

    project_id = context.app_cfg.get('project_id', None)
    assert project_id, "Project ID was not provided"

    cloud_storage_id = context.app_cfg.get('cloud_storage_id', None)
    assert cloud_storage_id, "Cloud storage ID was not provided"

    auth = HTTPBasicAuth(login, password)
    client = boto3.client(
            's3',
            aws_access_key_id=key_id,
            aws_secret_access_key=secret_key,
            endpoint_url=endpoint_url
    )

    df: pd.DataFrame = df # REMOVE
    results = {}
    data = requests.get(f'{cvat_url}/api/tasks', auth=auth)
    data =  json.loads(data.text)

    for d in data['results']:
        results[d['name']] = d['id']

    while data['next'] is not None:
        data = requests.get(data['next'], auth=auth)
        data =  json.loads(data.text)

        for d in data['results']:
            results[d['name']] = d['id']
    outputs = []
    task_names = df['task_name'].unique().tolist()
    for task_name in task_names:
        if task_name not in results.keys():
            print(f'Creating task {task_name}')
            task_id = requests.post(
                f'{cvat_url}/api/tasks',
                auth=auth,
                json={
                    'name': task_name,
                    'project_id': project_id
                }
            )
            task_id = json.loads(task_id.text)
            results[task_name] = task_id['id']
        images = df[df['task_name'] == task_name]['image'].to_list()

        for image in images:
            path = context.get_share_path(image)
            image_set = []
            client.upload_file(path, bucket_name, f'{task_name}/{image}')
            image_set.append(f'{task_name}/{image}')
            outputs.append([task_name, image])

        requests.post(
            f'{cvat_url}/api/tasks/{results[task_name]}/data',
            auth=auth,
            json={
                'image_quality': 100,
                'cloud_storage_id': cloud_storage_id,
                'server_files' : image_set,
                'storage': 'cloud_storage'
            }
        )

    return pd.DataFrame(outputs, columns=['task_name', 'image', 'status'])
