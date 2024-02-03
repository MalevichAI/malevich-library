import pandas as pd
from cvat_sdk.api_client import ApiClient, Configuration, models
from malevich.square import DF, Context, processor, scheme
from pydantic import BaseModel


@scheme()
class TaskImages(BaseModel):
    task: str
    image: str

@scheme()
class UploadResult(BaseModel):
    task: str
    image: str
    status: str

@processor()
def upload_images_to_task(df: DF[TaskImages], context: Context):
    """
        Creates task (if does not exists) and upload images to the task.

        Input:
            DF [TaskImages]:
                DataFrame which contains 2 columns:
                    - task: Name of the task where image should be uploaded
                    - image: Name of the image file

        Configuration:
        -  `cvat_user`, `cvat_password` - CVAT account credentials

        -  `cvat_url` - URL of your CVAT server

        -  `project_id` - ID of CVAT project


        Output:
            DF [UploadResult]:
                DataFrame which contains 3 columns:
                    task: Name of the task where image should be uploaded
                    image: Name of the image file
                    status: Upload Status Code
        Args:
            TaskImages: DF[TaskImages]:
                A DataFrame with image and corresponding task

        Returns:
            DF[UploadResult]:
                A DataFrame with status code of each image upload
    """  # noqa: E501
    login = context.app_cfg.get('cvat_user', None)
    password = context.app_cfg.get('cvat_password', None)
    assert login and password, "CVAT credentials were not provided"

    cvat_url = context.app_cfg.get('cvat_url', None)
    assert cvat_url, "CVAT link was not provided"

    project_id = context.app_cfg.get('project_id', None)
    assert project_id, "Project ID was not provided"

    cfg = Configuration(
        host=cvat_url,
        username=login,
        password=password
    )

    with ApiClient(cfg) as client:
        outputs = []
        task_names = df['task'].unique().tolist()
        for task_name in task_names:
            task_spec = models.TaskWriteRequest(
                name=task_name,
                project_id=project_id
            )
            task, _ = client.tasks_api.create(task_spec)
            images = df[df['task'] == task_name]['image'].to_list()

            image_set = []
            for image in images:
                path = context.get_share_path(image)
                image_set.append(open(path, 'rb'))

            data = models.DataRequest(
                image_quality=100,
                client_files=image_set,
                use_zip_chunks=True,
                use_cache=True
            )

            (_, response) = client.tasks_api.create_data(
                task.id,
                data_request=data,
                _content_type="multipart/form-data"
            )
            for image in images:
                outputs.append([task_name, image, response.status])

        result = pd.DataFrame(
            outputs,
            columns=['task', 'image', 'status']
        )

    return result
