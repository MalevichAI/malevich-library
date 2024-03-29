import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor

import boto3
import pandas as pd
from cvat_sdk.api_client import ApiClient, Configuration, models
from malevich.square import DF, Context, processor, scheme
from pydantic import BaseModel

from .models import UploadImagesToTask


@scheme()
class TaskImages(BaseModel):
    task: str
    image: str

@scheme()
class UploadResult(BaseModel):
    task: str
    image: str
    status: str

def upload_to_s3(
    key_id,
    secret_key,
    path,
    bucket_name,
    bucket_path,
    endpoint_url=None
):

    client = boto3.client(
        's3',
        aws_access_key_id=key_id,
        aws_secret_access_key=secret_key,
        endpoint_url=endpoint_url
    )

    client.upload_file(path, bucket_name, bucket_path)


@processor()
def upload_images_to_task(df: DF[TaskImages], context: Context[UploadImagesToTask]):
    """
    Creates task (if does not exists) and upload images to the task.

    ## Input:

        A dataframe with two columns:

        - task (string): Name of the task where image should be uploaded
        - image (string): Name of the image file

    ## Configuration:

        - `cvat_url`: str.
            URL of your CVAT server.

        - `cvat_user`: str.
            Account user name on CVAT.

        - `cvat_password`: str.
            Account user password on CVAT.

        - `cvat_org`: str, default ''.
            CVAT organization. By default uses personal workspace.

        - `project_id`: str.
			ID of CVAT project.

        - `cloud_id`: str.
			ID of cloud storage.

        - `aws_access_key_id`: str.
			AWS credentials.

        - `aws_secret_access_key`: str.
			AWS credentials.

        - `endpoint_url`: str, default 'AWS S3 endpoint'.
            URL endpoint of the cloud storage (S3).

        - `bucket_name`: str, default "cvat".
			Name of S3 bucket.


    ## Output:

        A dataframe with three columns:
        - task (string): Name of the task where image should be uploaded
        - image (string): Name of the image file
        - status (string): Upload Status Code

    -----
        Args:
            TaskImages: DF[TaskImages]:
                A DataFrame with image and corresponding task

        A dataframe with three columns:
            - task (string): Name of the task where image should be uploaded
            - image (string): Name of the image file
            - status (string): Upload Status Code
    -----

    Args:
        TaskImages: DF[TaskImages]:
            A DataFrame with image and corresponding task

    Returns:
        DF[UploadResult]:
            A DataFrame with status code of each image upload
    """  # noqa: E501
    login = context.app_cfg.get('cvat_user', None)
    password = context.app_cfg.get('cvat_password', None)
    org = context.app_cfg.get('cvat_org', "")
    assert login and password, "CVAT credentials were not provided"

    cvat_url = context.app_cfg.get('cvat_url', None)
    assert cvat_url, "CVAT link was not provided"

    project_id = context.app_cfg.get('project_id', None)
    assert project_id, "Project ID was not provided"

    cloud_id = context.app_cfg.get('cloud_id', None)
    assert cloud_id, "Cloud ID was not provided"

    aws_access_key_id = context.app_cfg.get('aws_access_key_id', None)
    aws_secret_access_key = context.app_cfg.get('aws_secret_access_key', None)
    assert (
        aws_access_key_id and aws_secret_access_key
    ), "AWS credentials were not provided"
    endpoint_url = context.app_cfg.get('endpoint_url', None)

    bucket_name = context.app_cfg.get('bucket_name', 'cvat')

    cfg = Configuration(
        host=cvat_url,
        username=login,
        password=password
    )

    with ApiClient(cfg) as client:
        outputs = []
        task_names = df['task'].unique().tolist()
        for task_name in task_names:
            executor = ProcessPoolExecutor(mp.cpu_count()//2)
            task_spec = models.TaskWriteRequest(
                name=task_name,
                project_id=project_id
            )
            task, _ = client.tasks_api.create(task_spec, org=org)
            images = df[df['task'] == task_name]['image'].to_list()

            image_set = []
            for image in images:
                path = context.get_share_path(image)
                executor.submit(
                    upload_to_s3,
                    key_id=aws_access_key_id,
                    secret_key=aws_secret_access_key,
                    path=path,
                    bucket_name=bucket_name,
                    bucket_path=f"{task_name}/{image}",
                    endpoint_url=endpoint_url
                )
                image_set.append(f"{task_name}/{image}")

            executor.shutdown(wait=True)

            data = models.DataRequest(
                image_quality=100,
                server_files=image_set,
                use_zip_chunks=True,
                use_cache=True,
                cloud_storage_id=cloud_id
            )

            (_, response) = client.tasks_api.create_data(
                task.id,
                data_request=data
            )
            for image in images:
                outputs.append([task_name, image, response.status])

        result = pd.DataFrame(
            outputs,
            columns=['task', 'image', 'status']
        )

    return result
