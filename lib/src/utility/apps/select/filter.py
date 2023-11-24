from malevich.square import DF, Any, Context, processor


@processor()
def filter(df: DF[Any], context: Context):
    """Filters rows by a number of conditions

    Inputs:
        An arbitrary dataframe to filter rows from

    Outputs:
        A filtered dataframe

    A single condition is a dictionary with the following keys:
    - column: the column to filter on
    - operation: the operation to perform
    - value: the value to filter on
    - type: the type of the value to filter on (optional)

    Example:
    {
        "conditions": [
            {
                "column": "age",
                "operation": "greater",
                "value": 18,
                "type": "int"
            },
            {
                "column": "name",
                "operation": "like",
                "value": "John"
            }
        ]
    }

    Supported operations:
    - equal
    - not_equal
    - greater
    - greater_equal
    - less
    - less_equal
    - in
    - not_in
    - like
    - not_like
    - is_null
    - is_not_null

    Supported types:
    - int
    - float
    - bool
    - str

    Args:
        df: the dataframe to filter rows from
        context: the context of the current request

    Returns:
        A filtered dataframe
    """
    conditions = context.app_cfg.get('conditions', [])

    for cond in conditions:
        column = cond['column']
        operator = cond['operation']
        value = cond['value']
        val_type = cond.get('type', 'str')

        if val_type == 'int':
            value = int(value)
        elif val_type == 'float':
            value = float(value)
        elif val_type == 'bool':
            value = bool(value)
        elif val_type == 'str':
            value = str(value)

        if operator == 'equal':
            df = df[df[column] == value]
        elif operator == 'not_equal':
            df = df[df[column] != value]
        elif operator == 'greater':
            df = df[df[column] > value]
        elif operator == 'greater_equal':
            df = df[df[column] >= value]
        elif operator == 'less':
            df = df[df[column] < value]
        elif operator == 'less_equal':
            df = df[df[column] <= value]
        elif operator == 'in':
            df = df[df[column].isin(value)]
        elif operator == 'not_in':
            df = df[~df[column].isin(value)]
        elif operator == 'like':
            df = df[df[column].str.contains(value)]
        elif operator == 'not_like':
            df = df[~df[column].str.contains(value)]
        elif operator == 'is_null':
            df = df[df[column].isna()]
        elif operator == 'is_not_null':
            df = df[df[column].notna()]

    return df
