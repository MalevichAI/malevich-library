from typing import Any, List
from jls import jls, Context, DFS, M, DF
import pandas as pd


def merge_dfs(dfs: List[DF[Any]], context: Context):
    # TODO: Document code
    how = context.app_cfg.get('how', 'inner')
    on = context.app_cfg.get('both_on', ('index' if how != 'cross' else None))
    left_on = context.app_cfg.get('left_on', None)
    right_on = context.app_cfg.get('right_on', None)
    suffixes = context.app_cfg.get('suffixes', ['_0', '_1'])
    
    flatten_dfs = []
    for x in dfs:
        for y in x:
            flatten_dfs.append(y)

    result: pd.DataFrame = flatten_dfs[0]
    
    for i in range(1, len(flatten_dfs)):
        kwargs = {}
        if left_on is not None:
            if left_on == 'index':
                kwargs['left_index'] = True
            else:
                kwargs['left_on'] = left_on
        if right_on is not None:
            if right_on == 'index':
                kwargs['right_index'] = True
            else:
                kwargs['right_on'] = right_on
        if on is not None:
            if on == 'index':
                kwargs['left_index'] = True
                kwargs['right_index'] = True
            else:
                kwargs['on'] = on
                
        result = result.merge(flatten_dfs[i], how=how, suffixes=suffixes, **kwargs)
        
    return result
    

@jls.processor()
def merge(dfs: DFS[M[Any]], context: Context):
    return merge_dfs(list(iter(dfs)), context)



@jls.processor()
def merge_2(df_1: DF[Any], df_2: DF[Any], context: Context):
    """Simplify sink_2 -> merge"""
    return merge_dfs([(df_1,), (df_2,)], context)


@jls.processor()
def merge_3(df_1: DF[Any], df_2: DF[Any], df_3: DF[Any], context: Context):
    """Simplify sink_3 -> merge"""
    return merge_dfs([(df_1,), (df_2,), (df_3,)], context)

