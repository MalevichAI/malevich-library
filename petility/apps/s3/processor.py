import os
from jls import jls, Context, DF, DFS, M, S3Helper, APP_DIR
from typing import Any
from pydantic import BaseModel

import pandas as pd


@jls.scheme()
class filename_s3key(BaseModel):
    filename: str
    s3key: str
    
    
@jls.scheme()
class filename(BaseModel):
    filename: str


@jls.processor()
def save_dfs(dfs: DFS[M[Any]], context: Context):
    """Saves received dataframes to S3.
    
    Saving is controlled by the following configuration parameters:
        - names: list or str
            If list, it should contain the names of the dataframes to be saved. If
            the list is shorter than the number of dataframes, the remaining dataframes
            will be named 'df_{i}' where i is the index of the dataframe. If str, it
            should be a format string that will be used to name the dataframes. 

            Format variables:
                - {ID}: index of the dataframe
    
        - append_run_id: bool
            If True, the run_id will be appended to the name of the dataframe. In
            other words, it will be saved in a folder named after the run_id.
            
        
    Examples:
        # Examples are not an actual code. They are just to show how the configuration
        # parameters work.
        
        config = {
            'names': ['df1', 'df2', 'df3'],
            'append_run_id': True
        }
        
        save_dfs([D1, D2, D3, D4], config)
        
        # D1 will be saved as {run_id}/df1
        # D2 will be saved as {run_id}/df2
        # D3 will be saved as {run_id}/df3
        # D4 will be saved as {run_id}/df_4
        
        config = {
            'names': 'df_{ID}',
            'append_run_id': False
        }
        
        save_dfs([D1, D2, D3, D4], config)
        
        # D1 will be saved as df_0
        # D2 will be saved as df_1
        # D3 will be saved as df_2
        # D4 will be saved as df_3    
    """
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
            
        
@jls.processor()
def save_files_auto(files: DF['filename'], context: Context):
    """Saves files from local file system to S3.
    
    Saving is controlled by the following configuration parameters:
        - append_run_id: bool
        
    This processor is similar to `save_files` but it does not require the user to
    specify the S3 key for each file. Instead, it uses the filename as the S3 key.
        
    Args:
        files: 
            A dataframe with a column named 'filename' that contains the names
            of the files to be saved. Files are expected to be in the share folder 
            e.g. should be shared with `context.share(<FILE>)` before.
            
    Returns:
        The same dataframe as the input with an additional column named 's3key'
        that contains the S3 key for each file.
    """
    # Initializing an object to interact with S3
    s3_helper: S3Helper = context.app_cfg['s3_helper']
    s3_keys = []
    for file in files['filename']:
        extra_str = f'{context.app_cfg["extra_str"]}/' if 'extra_str' in context.app_cfg else ''
        run_id = f'{context.run_id}/' if context.app_cfg.get('append_run_id', False) else ''
        # Get share path with default prefix (APP_DIR)
        key = f'{extra_str}{run_id}{file}'
        # key = f'{context.run_id}/{file}' if context.app_cfg.get('append_run_id', False) else file
        with open(context.get_share_path(file), 'rb') as f:
            s3_helper.save_object(f, key=key)
            s3_keys.append(key)
            
    files.insert(column='s3key', value=s3_keys, loc=len(files.columns))
    return files
    
    
@jls.processor()
def save_files(files: DF['filename_s3key'], context: Context):
    """Saves files from local file system to S3.
    
    This processor is similar to `save_files_auto` but it requires the user to
    specify the S3 key for each file.
    
    This processor is not configurable and does not use any configuration parameters.
    
    Args:
        files:
            A dataframe with two columns: 'filename' and 's3key'. 'filename' contains
            the names of the files to be saved. Files are expected to be in the share
            folder e.g. should be shared with `context.share(<FILE>)` before. 's3key'
            contains the S3 key for each file.
            
    Returns:
        The same dataframe as the input.
    """
    s3_helper: S3Helper = context.app_cfg['s3_helper']
    
    for file, s3_key in files[['filename', 's3key']].itertuples(index=False):
        with open(context.get_share_path(file), 'rb') as f:
            s3_helper.save_object(f, key=s3_key)
            
    return files
            
            
@jls.processor()
def download_files(files: DF['filename_s3key'], context: Context):
    """Downloads files from S3 to local file system.
    
    Args:
        files:
            A dataframe with two columns: 'filename' and 's3key'. 'filename' contains
            the names of the files to be saved. 's3key' contains the S3 key for each
            file.
            
    Returns:
        The same dataframe as the input.
    """
    s3_helper: S3Helper = context.app_cfg['s3_helper']
    
    output_files = []
    for file, s3_key in files[['filename', 's3key']].itertuples(index=False):
        fbytes = s3_helper.get_object(s3_key)
        with open(os.path.join(APP_DIR, file), 'wb+') as f:
            f.write(fbytes.read())
            context.share(file)
            output_files.append(file)
            
    return pd.DataFrame({
        'filename': output_files,
    })
            
            
        