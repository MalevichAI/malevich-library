import os
from hashlib import sha256
from typing import Any

import pandas as pd
from malevich.square import APP_DIR, DF, DFS, Context, M, S3Helper, processor, scheme
from pydantic import BaseModel

from .models import (
    S3DownloadFiles,
    S3DownloadFilesAuto,
    S3Save,
    S3SaveFiles,
    S3SaveFilesAuto,
)


@scheme()
class FilenameS3Key(BaseModel):
    filename: str
    s3key: str

@scheme()
class S3Key(BaseModel):
    s3key: str

@scheme()
class Filename(BaseModel):
    filename: str


@processor()
def s3_save(dfs: DFS[M[Any]], context: Context[S3Save]):
    """Saves dataframes to S3.

    ## Input:
        dfs: Multiple dataframes to be saved.

    ## Configuration:
        - `names`: list[str]|str.
            Names of the dataframes to be saved.
            If a list is provided, it should have the same length as the number of dataframes.
            If a string is provided, it is used as a format string to generate the names of the dataframes.
            Available format variables:
                {ID}: index of the dataframe
            If the number of dataframes is greater than the length of the list or
            the number of format variables in the string, default names are used
            for the remaining dataframes.
        - `append_run_id`: bool, default False.
            If True, the run_id is appended to the names of the dataframes.
        - `extra_str`: str, default None.
            If provided, it is appended to the names of the dataframes.

        Also, the app should be provided with parameters to connect to S3:
        - `aws_access_key_id`: str.
            AWS access key ID.
        - `aws_secret_access_key`: str.
            AWS secret access key.
        - `bucket_name`: str.
            Name of the S3 bucket.
        - `endpoint_url`: str, default None.
            Endpoint URL of the S3 bucket.
        - `aws_region`: str, default None.
            AWS region of the S3 bucket.

    ## Details:
        This processor saves dataframes to S3. User can provide names for the
        dataframes to be saved. If no names are provided, default names are used.
        If the number of dataframes is greater than the length of the list of names
        or the number of format variables in the string, default names are used
        for the remaining dataframes.

        If `append_run_id` is True, the run_id is appended to the names of the
        dataframes. If `extra_str` is provided, it is appended to the names of
        the dataframes.

        The dataframes are saved to S3 using the following key:
            <EXTRA_STR>/<RUN_ID>/<NAME>

        A common use case of extra_str is to save dataframes to different folders
        within the S3 bucket. For example, if extra_str is 'train', the dataframes
        are saved to the following key:

            train/<RUN_ID>/<NAME>

    ## Output:
        The same as the input.

    -----

    Args:
        dfs: DFS containing DataFrames to be saved.

    Returns:
        The same dataframes as the input.

    """  # noqa: E501
    # Initializing an object to interact with S3
    s3_helper: S3Helper = context.app_cfg['s3_helper']

    # Getting the names of the dataframes
    name_expr = context.app_cfg['names']

    # Final names to be computed
    names = []

    # If the names are provided as a list, they are used as is
    # If the list is shorter than the number of dataframes, default names are used
    # for the remaining dataframes
    if isinstance(name_expr, list):
        # Slice the list to the length of the dataframes
        names = name_expr[:min(len(name_expr), len(dfs))]

        if len(names) < len(dfs):
            # Use default names for the remaining dataframes
            names += [f'df_{i + 1}' for i in range(len(names), len(dfs))]

    # If the names are provided as a string, they are used as a format string
    elif isinstance(name_expr, str):
        # Available format variables:
        #   - {ID}: index of the dataframe
        if '{ID}' in name_expr:
            names = [name_expr.format(ID=i) for i in range(len(dfs))]
        else:
            names = [name_expr + f'_{i + 1}' for i in range(len(dfs))]

    # If `append_run_id` is True, the run_id is appended to the names
    if context.app_cfg.get('append_run_id', False):
        names = [f'{context.run_id}/{name}' for name in names]

    if (extra := context.app_cfg.get('extra_str', None)):
        names = [f'{extra}/{name}' for name in names]

    # Save the dataframes
    for df, save_name in zip(dfs[0], names):
        # [! ] dfs[0] is a list of dataframes
        # as all members of DFS are also DFS
        # (preserving homogeneity of the data structure)
        s3_helper.save_df(df, key=save_name)
    # Return the dataframes as is
    # (similar to utility.passthrough)
    return dfs


@processor()
def s3_save_files_auto(files: DF['Filename'], context: Context[S3SaveFilesAuto]):
    """Saves files from local file system to S3 preserving the original names.

    ## Input:

        A dataframe with one column:
            - `filename` (str): Contains the names of the files to be saved.

    ## Configuration:
        - `append_run_id`: bool, default False.
            If True, the run_id is appended to the names of the files.
        - `extra_str`: str, default None.
            If provided, it is appended to the names of the files.

        Also, the app should be provided with parameters to connect to S3:
        - `aws_access_key_id`: str.
            AWS access key ID.
        - `aws_secret_access_key`: str.
            AWS secret access key.
        - `bucket_name`: str.
            Name of the S3 bucket.
        - `endpoint_url`: str, default None.
            Endpoint URL of the S3 bucket.
        - `aws_region`: str, default None.
            AWS region of the S3 bucket.

    ## Details:
        Files are expected to be in the share folder e.g. should be shared with
        `context.share(<FILE>)` before by a previous processor.

        The files are saved to S3 using the following key:
            <EXTRA_STR>/<RUN_ID>/<SHARED_FILE_NAME>

        A common use case of extra_str is to save files to different folders
        within the S3 bucket. For example, if extra_str is 'train', the files
        are saved to the following key:

                train/<RUN_ID>/<SHARED_FILE_NAME>

    ## Output:
        The same as the input.

    -----

    Args:
        files: DF containing filenames to be saved.

    Returns:
        The same dataframe as the input.
    """
    # Initializing an object to interact with S3
    s3_helper: S3Helper = context.app_cfg['s3_helper']
    s3_keys = []
    for file in files['filename']:
        extra_str = \
            f'{context.app_cfg["extra_str"]}/' if 'extra_str' in context.app_cfg else ''
        run_id = \
            f'{context.run_id}/' if context.app_cfg.get('append_run_id', False) else ''
        # Get share path with default prefix (APP_DIR)
        key = f'{extra_str}{run_id}{file}'
        # key = f'{context.run_id}/{file}'
        # if context.app_cfg.get('append_run_id', False) else file
        with open(context.get_share_path(file), 'rb') as f:
            s3_helper.save_object(f, key=key)
            s3_keys.append(key)

    files.insert(column='s3key', value=s3_keys, loc=len(files.columns))
    return files


@processor()
def s3_save_files(files: DF['FilenameS3Key'], context: Context[S3SaveFiles]):
    """Saves files from local file system to S3.

    ## Input:
        A dataframe with columns:
        - `filename` (str): the names of the files to be saved.
        - `s3key` (str): the S3 key for each file.

    ## Configuration:
        - `append_run_id`: bool, default False.
            If True, the run_id is appended to the names of the files.

        Also, the app should be provided with parameters to connect to S3:
        - `aws_access_key_id`: str.
            AWS access key ID.
        - `aws_secret_access_key`: str.
            AWS secret access key.
        - `bucket_name`: str.
            Name of the S3 bucket.
        - `endpoint_url`: str, default None.
            Endpoint URL of the S3 bucket.
        - `aws_region`: str, default None.
            AWS region of the S3 bucket.

    ## Details:
        Files are expected to be in the share folder e.g. should be shared with
        `context.share(<FILE>)` before by a previous processor.

        The files are saved to S3 using the following key:
            <EXTRA_STR>/<RUN_ID>/<S3_KEY>

        A common use case of extra_str is to save files to different folders
        within the S3 bucket. For example, if extra_str is 'train', the files
        are saved to the following key:

                train/<RUN_ID>/<S3_KEY>

        S3 keys might contain following variables:
            - {ID}: index of the dataframe
            - {FILE}: base filename, for example 'file.csv' for 'path/to/file.csv'
            - {RUN_ID}: run_id

        For example, if the S3 key is 'train/{RUN_ID}/{FILE}', file name is 'file.csv',
        run_id is 'run_1', the file will be saved to 'train/run_1/file.csv'.

    ## Output:
        The same as the input.

    -----

    Args:
        files: DF containing filenames to be saved.

    Returns:
        The same dataframe as the input.
    """
    s3_helper: S3Helper = context.app_cfg['s3_helper']

    for i, (file, s3_key) in files[['filename', 's3key']].itertuples():
        with open(context.get_share_path(file), 'rb') as f:
            s3_key = s3_key.format(
                ID=i,
                FILE=os.path.basename(file),
                RUN_ID=context.run_id
            )
            s3_helper.save_object(f, key=s3_key)

    return files


@processor()
def s3_download_files(files: DF['FilenameS3Key'], context: Context[S3DownloadFiles]):
    """Downloads files from S3 to local file system.

    ## Input:
        A dataframe with columns:
        - `filename` (str): the names of the files to be saved.
        - `s3key` (str): the S3 key for each file.

    ## Configuration:

        The app's only configuration is the connection to S3:
        - `aws_access_key_id`: str.
            AWS access key ID.
        - `aws_secret_access_key`: str.
            AWS secret access key.
        - `bucket_name`: str.
            Name of the S3 bucket.
        - `endpoint_url`: str, default None.
            Endpoint URL of the S3 bucket.
        - `aws_region`: str, default None.
            AWS region of the S3 bucket.

    ## Details:
       Files are downloaded by their S3 keys. The files are shared across processors
       under keys specified by `filename` column.

       For example, for the dataframe:
            | filename  |            s3key          |
            | --------  |            -----          |
            | file1.csv | path/to/some_file.csv     |

            The file is assumed to be in S3 under the key `path/to/some_file.csv`.
            The file is downloaded from S3 and shared under the key `file1.csv`.

    ## Output:
        The dataframe with downloaded filenames.

    -----

    Args:
        files: DF containing filenames to be downloaded.

    Returns:
        The dataframe with downloaded filenames.
    """

    s3_helper: S3Helper = context.app_cfg['s3_helper']

    output_files = []
    for file, s3_key in files[['filename', 's3key']].itertuples(index=False):
        fbytes = s3_helper.get_object(s3_key)
        with open(os.path.join(APP_DIR, file), 'wb+') as f:
            for byte_ in fbytes:
                f.write(byte_)
        context.share(file)
        output_files.append(file)

    return pd.DataFrame({
        'filename': output_files,
    })


@processor()
def s3_download_files_auto(keys: DF[S3Key], context: Context[S3DownloadFilesAuto]):
    """Downloads files from S3 to local file system.

    ## Input:
        A dataframe with columns:
        - `s3key` (str): the S3 key for each file.

    ## Configuration:

        The app's only configuration is the connection to S3:

        - `aws_access_key_id`: str.
            AWS access key ID.
        - `aws_secret_access_key`: str.
            AWS secret access key.
        - `bucket_name`: str.
            Name of the S3 bucket.
        - `endpoint_url`: str, default None.
            Endpoint URL of the S3 bucket.
        - `aws_region`: str, default None.
            AWS region of the S3 bucket.

    ## Output:
        A dataframe with columns:
            - s3key (str): S3 key of the file
            - filename (str): The name of the file

    -----

    Args:
        keys: DF containing keys of the files to be downloaded.

    Returns:
        A dataframe with columns:
            - s3key (str): S3 key of the file
            - filename (str): The name of the file
    """
    s3_helper: S3Helper = context.app_cfg['s3_helper']

    output_files = []
    for s3_key in keys['s3key'].to_list():
        fbytes = s3_helper.get_object(s3_key)
        extension = os.path.splitext(s3_key)[1]
        file = context.run_id + '-' + sha256(s3_key.encode()).hexdigest() + extension
        with open(os.path.join(APP_DIR, file), 'wb+') as f:
            for byte_ in fbytes:
                f.write(byte_)
        context.share(file)
        output_files.append([s3_key, file])
    return pd.DataFrame(
        output_files, columns = ['s3_key', 'filename']
    )
