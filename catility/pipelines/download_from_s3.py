import argparse
import boto3
import uuid
import random
import tempfile
from jls_utils import *


parser = argparse.ArgumentParser()

parser.add_argument('-i')
parser.add_argument('-H', default='http://localhost:8080')
parser.add_argument('-b', '--bucket', required=True)
parser.add_argument('-id', '--aws_key_id', required=True)
parser.add_argument('-s', '--aws_secret', required=True)
parser.add_argument('-e', '--endpoint', default=None)


def random_string():
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=256))


if __name__ == '__main__':
    args = parser.parse_args()

    update_core_credentials('library', 'library')
    set_host_port(args.H)

    try: delete_user()
    except: pass
    finally: create_user()

    config = {
        'aws_access_key_id': args.aws_key_id,
        'aws_secret_access_key': args.aws_secret,
        'endpoint_url': args.endpoint,
        'bucket_name': args.bucket
    }
    
    id = str(uuid.uuid4())
    client = boto3.client(
        's3',
        aws_access_key_id=args.aws_key_id,
        aws_secret_access_key=args.aws_secret,
        endpoint_url=args.endpoint
    )
    
    with tempfile.NamedTemporaryFile('w') as f:
        f.write(random_string())
        f.flush()
        client.upload_file(f.name, args.bucket, f'{id}/test.txt')
        print(f'Uploaded file {f.name} to {args.bucket}/{id}/test.txt')

    filename_s3_collection = create_collection_from_df(
        pd.DataFrame({
            'filename': [f'test.txt'],
            's3key': [f'{id}/test.txt']
        })
    ) 
    
    create_scheme({
        "type": "object",
        "properties": {
            "filename": {
                "type": "string"
            },
            "s3key": {
                "type": "string"
            }
        }
    }, 'filename_s3key')
    
    
    create_scheme({
        "type": "object",
        "properties": {
            "filename": {
                "type": "string"
            },
        }
    }, 'filename')
    

    create_app(
        app_id='download_files',
        input_id='download_from_collection',
        processor_id='download_files',
        image_ref='utility',
        app_cfg={
            **config,
        }
    )
    
    create_app(
        app_id='select_filenames',
        processor_id='locs',
        app_cfg={
            'column': 'filename'
        },
        image_ref='utility'
    )
    
    
    create_app(
        app_id='save_files_auto',
        processor_id='save_files_auto',
        app_cfg={
            'append_run_id': True,
            'extra_str': 'some_file_name',
            **config,
        },
        image_ref='utility'
    )    
    
    
    create_task(
        task_id='select_filenames',
        app_id='select_filenames',
        apps_depends=['download_files']
    )
    
    create_task(
        task_id='save_files_auto',
        app_id='save_files_auto',
        tasks_depends=['select_filenames']
    )
    
    try:
        client.delete_object(Bucket=args.bucket, Key=f'{id}/test.txt')
        client.delete_object(Bucket=args.bucket, Key=f'{id}/')
    except:
        pass    
    
    cfg = Cfg(
        collections={
            'download_filename_s3': filename_s3_collection
        },
        init_apps_update={
            'connect_to_s3': True
        }
    )
     
    
    create_cfg('main_cfg', cfg)
    task_full('save_files_auto', 'main_cfg', with_show=True, profile_mode='df_show')