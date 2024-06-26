import re

import pandas as pd
import sqlalchemy as sql
from malevich.square import DF, DFS, Context, processor, scheme
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError

from .models import Query


@scheme()
class ExecuteMessage(BaseModel):
    command: str

@scheme()
class FormatTokenMessage(BaseModel):
    token: str
    value: str

@processor()
def executemany(
    exec_msg: DF[ExecuteMessage],
    fmt_msg: DF[FormatTokenMessage],
    ctx: Context[Query]
) -> DFS:
    '''
    Execute raw SQL commands on the database.
    If your command utilizes placeholders, refer to `executemany` processor.

    ## Input:

        Consists of two dataframes.

        `exec_msg` (DF[ExecuteMessage]): A dataframe with columns:
            - `command` (str): command string.

        `fmt_msg` (DF[FormatTokenMessage]): A dataframe with format values for tokens in the commands:
            - `token` (str): token in the command.
            - `value` (str): substitute string.

    ## Output:

        A list of dataframes with a result for each query. If the query does not return any values, a dataframe with a single column `rows_affected` is returned.


    ## Configuration:

        - `url`: str.
            URL of the DB to connect to.
        - `subsequent`: bool.
            if True, each statement will be commited before the next one is executed.


    ## Notes:

        IMPORTANT! Format tokens are needed for literals such as table names and column names.

        E.g. for queries:
        ```sql
        CREATE TABLE IF NOT EXISTS {table} (
                {column_1} INTEGER PRIMARY KEY,
                {column_2} TEXT,
                {column_3} INTEGER
            );
        ```

        The format tokens needed can look like this:
        ----------------------
        | token    | value   |
        ----------------------
        | table    | products|
        | column_1 | id      |
        | column_2 | name    |
        | column_3 | price   |
        ----------------------

    -----

    Args:

        exec_msg (DF[ExecuteMessage]): dataframe with commands
        fmt_msg (DF[FormatTokenMessage]): dataframe with format tokens

    Returns:

        DF[Any]: result of the query or the number of rows affected by a query
    ''' # noqa:E501
    session_url = ctx.app_cfg.url
    subsequent = ctx.app_cfg.subsequent

    with sql.create_engine(session_url).connect() as conn:
        try:
            result: list[pd.DataFrame] = []

            for id, command in enumerate(exec_msg.to_dict(orient='records')):
                # Selecting needed format values
                pattern = r'\{(.*?)\}'
                tokens = re.findall(pattern, command['command'], flags=re.MULTILINE)
                fmt = fmt_msg[fmt_msg.token.isin(tokens)].to_dict(orient='records')
                kv_fmt = {
                    msg['token'] : msg['value']
                    for msg in fmt
                }
                # Selecting placeholders and validating the shape
                ret = conn.execute(sql.text(command['command'].format(**kv_fmt)))
                if ret.returns_rows:
                    result.append(
                        pd.DataFrame(ret.all(), columns=ret.keys())
                    )
                else:
                    result.append(
                        pd.DataFrame(
                            data={
                                'rows_affected': [ret.rowcount]
                            }
                        )
                    )

                if subsequent:
                    conn.commit()

            if not subsequent:
                conn.commit()

        except SQLAlchemyError as sexc:
            conn.rollback()
            raise Exception('Query error! Please check all of the statements') from sexc

        except Exception as exc:
            raise Exception('Please check the input collections') from exc

    return result
