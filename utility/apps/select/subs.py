from typing import Any
from jls import jls, DF, DFS, M, Context


@jls.processor(id='subset')
def subset(dfs: DFS[M[Any]], context: Context):
    """Retrieves a subset of dataframes passed from a single application.
    
    The behaviour is controlled using the app configuration (`expr` field)
    Use the following syntax: 
        slice_begin
        slice_begin:slice_end (inclusive)
        slice_begin:slice_end,...
        
    Example:
        0 -- Retrieve only the first dataframe
        0:1 -- Retrieve the first and the second dataframes
        0:1,3 -- Retrieve the first, the second and the fourth dataframes
        0:1,3:5,7 -- Retrieve dataframes 0, 1, 3, 4, 5 and 7

    Args:
        dfs (DFS[M[Any]]): List of dataframes
        context (Context): App Configuration
    """
    # Parse `expr` field of the configuration
    expr = context.app_cfg.get("expr", None)
    if expr is None:
        raise ValueError("The app configuration should contain `expr` field")
    
    # Split the expression by comma
    exprs = expr.split(",")
    
    # Initialize the result
    result = []
    
    # Iterate over the expressions
    for expr in exprs:
        # Split the expression by colon
        expr = expr.split(":")
        
        # If the expression contains only one element, 
        # it means that we should retrieve only one dataframe
        if len(expr) == 1:
            result.append(dfs[0][int(expr[0])])
        # Otherwise, we should retrieve a slice of dataframes
        else:
            result.extend(dfs[0][int(expr[0]):int(expr[1])])
            
    if len(result) == 1:
        return result[0]
    
    return result