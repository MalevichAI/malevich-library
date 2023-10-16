import boto3
from jls import Context, S3Helper, jls


@jls.init()
def connect_to_s3(context: Context):
    if not all([
        'aws_access_key_id' in context.app_cfg,
        'aws_secret_access_key' in context.app_cfg,
        'bucket_name' in context.app_cfg
    ]):
        # If any of the required parameters is missing, we disable the init function
        # and return. This way, the user can still use the app
        return

    aws_access_key_id = context.app_cfg['aws_access_key_id']
    aws_secret_access_key = context.app_cfg['aws_secret_access_key']
    endpoint_url = context.app_cfg.get('endpoint_url', None)
    bucket_name = context.app_cfg['bucket_name']
    region = context.app_cfg.get('aws_region', None)

    client = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        endpoint_url=endpoint_url,
        region_name=region
    )

    context.app_cfg['s3_helper'] = S3Helper(client, bucket_name)

