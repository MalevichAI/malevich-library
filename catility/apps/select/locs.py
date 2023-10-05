from jls import jls, Context
import pandas as pd


@jls.processor(id='locs')
def locs(df, context: Context):
    """(Loc)ate (s)tatically extracts a subset of the dataframe

    This function highly depends on the app configuration and 
    thus claimed to be static. It is used to extract a subset of
    the dataframe for further processing.

    Args:
        df (pd.DataFrame): The dataframe to be processed
        context (Context): 
            The context object. 

            The app_cfg attribute of the context object should 
            contain at least one of the following fields:
                - column: str - The column to be extracted
                - columns: list[str] - The columns to be extracted
                - column_idx: int - The column index to be extracted
                - column_idxs: list[int] - The column indexes to be extracted
                - row: int - The row to be extracted
                - rows: list[int] - The rows to be extracted
                - row_idx: int - The row index to be extracted
                - row_idxs: list[int] - The row indexes to be extracted

            In case of multiple fields are provided, the function
            will extract the intersection of the fields. 


    Returns:
        pd.DataFrame: The extracted dataframe
            
    """
    should_have = ['column', 'columns', 'column_idx', 'column_idxs',
                     'row', 'rows', 'row_idx', 'row_idxs']
    
    
    if not any([field in context.app_cfg for field in should_have]):
        raise ValueError(f'At least one of the following fields should be provided: {should_have}')
    

    # Extract the fields from the context object
    # to make the code more readable and avoid
    # multiple calls to the context object

    column = context.app_cfg.get('column', None)
    columns = context.app_cfg.get('columns', None)
    column_idx = context.app_cfg.get('column_idx', None)
    column_idxs = context.app_cfg.get('column_idxs', None)
    row = context.app_cfg.get('row', None)
    rows = context.app_cfg.get('rows', None)
    row_idx = context.app_cfg.get('row_idx', None)
    row_idxs = context.app_cfg.get('row_idxs', None)


    # Copy the dataframe to avoid side effects
    result: pd.DataFrame = df.copy()

    # ________________________________________________


    # We start with column id as it is the most specific
    # and thus the most restrictive
    if column_idx is not None and len(result.columns) > column_idx:
        result = pd.DataFrame(result.iloc[:, column_idx])
    elif column_idxs is not None:
        # Multiple indices are only processed if 
        # column_id is not provided to keep 
        # indices consistent

        # Filter only those indices that are in the dataframe
        # to tolerate missing columns
        column_idxs = [
            idx for idx in column_idxs 
            if len(result.columns) > idx
        ]

        result = pd.DataFrame(result.iloc[:, column_idxs])


    # ________________________________________________

        
    if column is not None and column in result.columns:
        result = pd.DataFrame(result[column])

    if columns is not None:
        # Multiple columns are only processed if 
        # column is not provided to keep 
        # indices consistent

        # Filter only those columns that are in the dataframe
        # to tolerate missing columns
        columns = [
            col for col in columns 
            if col in result.columns
        ]

        result = pd.DataFrame(result[columns])

    
    # ________________________________________________

    # We continue with row id as it is the most specific
    # and thus the most restrictive

    if row_idx is not None and len(result) > row_idx:
        result = pd.DataFrame(result.iloc[[row_idx], :])
    elif row_idxs is not None:
        # Multiple indices are only processed if 
        # row_id is not provided to keep 
        # indices consistent

        # Filter only those indices that are in the dataframe
        # to tolerate missing rows
        row_idxs = [
            idx for idx in row_idxs 
            if len(result) > idx
        ]

        result = pd.DataFrame(result.iloc[row_idxs, :])


    # ________________________________________________

    if row is not None and row in result.index:
        result = pd.DataFrame(result.loc[[row]])

    if rows is not None:
        # Multiple rows are only processed if 
        # row is not provided to keep 
        # indices consistent

        # Filter only those rows that are in the dataframe
        # to tolerate missing rows
        rows = [
            row for row in rows 
            if row in result.index
        ]

        result = pd.DataFrame(result.loc[rows])

    if context.app_cfg.get('print', False):
        print(result.head())

    return pd.DataFrame(result)


