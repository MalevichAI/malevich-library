from typing import Any, List

import pandas as pd
from malevich.square import DF, Context, Sink, processor

from .models import Merge


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


@processor()
def merge(dfs: Sink[Any], context: Context[Merge]):
    """Merges multiple dataframes into one

    ## Input:
        An iterable containing multiple dataframes to be merged.

    ## Configuration:
        - `how`: str, default 'inner'.
            The type of merge to be performed.

            Possible values:
                'inner':
                    Use intersection of keys from both frames,
                    similar to a SQL inner join;
                'outer':
                    Use union of keys from both frames,
                    similar to a SQL full outer join;
                'left':
                    Use only keys from left frame,
                    similar to a SQL left outer join;
                'right':
                    Use only keys from right frame,
                    similar to a SQL right outer join;
                'cross':
                    Create a cartesian product from both frames,
                    similar to a SQL cross join.

        - `both_on`: str|tuple, default ''.
            Column name or 'index' to merge on. If 'index', the index of the dataframe will be used. If column name, the column should be present in all dataframes.
        - `left_on`: str|list, default ''.
            Column name or 'index' to join on in the left DataFrame. If 'index', the index of the dataframe will be used. If column name, the column should be present in all but last dataframes.
        - `right_on`: str|list, default ''.
            Column name or 'index' to join on in the right DataFrame. If 'index', the index of the dataframe will be used. If column name, the column should be present in all but first dataframes.
        - `suffixes`: tuple, default ('_0', '_1').
            Suffix to apply to overlapping column names in the left and right dataframes.

    ## Output:
        Merged DataFrame

    ## Notes:
        If both 'both_on' and 'left_on/right_on' are provided,
        'both_on' will be ignored.

        Dataframes are merged iteratively from left to right.

        If using left_on column, all dataframes except
        the last one should have the column.

        If using right_on column, all dataframes except
        the first one should have the column.

    -----

    Args:
        dfs: DFS containing DataFrames to be merged.

    Returns:
        The merged dataframe
    """  # noqa: E501
    return merge_dfs(list(iter(dfs)), context)
