from jls import jls, Context, DF, Any


@jls.processor()
def add_column(df: DF[Any], context: Context):
    """Inserts a into a dataframe
    
    Inserts a column with a constant value into a dataframe at specified position.
    The behaviour is controlled by the following parameters in the app config:
        - column_name: name of the new column
        - value: value of the new column
        - position: position of the new column
    """
    column_name = context.app_cfg.get('column_name', 'new_column')
    value = context.app_cfg.get('value', 'new_value')
    position = context.app_cfg.get('position', 0)

    if position < 0:
        position = len(df.columns) + position + 1

    df.insert(position, column_name, value)
    
    return df
