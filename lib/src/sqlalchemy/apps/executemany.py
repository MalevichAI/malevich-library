import re
from typing import Any

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
class PlaceholderMessage(BaseModel):
    cmd_id: int
    token: str
    value: Any


@processor()
def executemany(
    exec_msg: DF[ExecuteMessage],
    plh_msg: DF[PlaceholderMessage],
    ctx: Context[Query]
) -> DFS:
    '''
    Execute raw SQL commands on the database with many values. Use this only if you need to run same commands with different parameters, since placeholder dataframe is mandatory.
    If your command does not utilize placeholders, refer to `execute` processor


    ## Input:

        Consists of two dataframes.

        `exec_msg` (DF[ExecuteMessage]): A dataframe with column:
            - `command` (str): command string.

        `plh_msg` (DF[PlaceholderMessage]): A dataframe with placeholders for the commands to execute multiple statements:
            - `cmd_id` (int): id of the command in `exec_msg` dataframe.
            - `token` (str): name of the token to substitute with.
            - `value`: value to substitute.

    ## Output:

        A list of dataframes with a result for each query. If the query does not return any values, a dataframe with a single column `rows_affected` is returned.


    ## Configuration:

        - `url`: str.
            URL of the DB to connect to.
        - `subsequent`: bool, default False.
            if True, each statement will be commited before the next one is executed.
        - `format`: dict, default None.
            Dictionary consisting of key-value pairs `token`:`value` that substitute tokens in the command.

    ## Notes:

        IMPORTANT! Format tokens are needed for literals such as table names and column names. Placeholders are needed for
        constants and help to execute a command multiple times. In order to use placeholders, mark the tokens in your SQL commands with `:`.

        E.g. for queries:
        ```sql
        CREATE TABLE IF NOT EXISTS {table} (
                {column_1} INTEGER PRIMARY KEY,
                {column_2} TEXT,
                {column_3} INTEGER
            );
        ```
        ```sql
        INSERT INTO {table} ({column_2}, {column_3})
            VALUES (:name, :price);
        ```

        The format tokens needed can look like this:
        ```
        {
            "table" : "products",
            "column_1" : "id",
            "column_2" : "name",
            "column_3" : "price"
        }
        ```

        And placeholders can look like this:
        --------------------------------
        | cmd_id | token | value       |
        --------------------------------
        | 1      | name  | product_name|
        | 1      | price |  200        |
        --------------------------------


    -----

    Args:

        exec_msg (DF[ExecuteMessage]): dataframe with commands
        fmt_msg (DF[FormatTokenMessage]): dataframe with format tokens
        plh_msg (DF[PlaceholerMessage]): dataframe with placeholders

    Returns:

        DF[Any]: result of the query or the number of rows affected by a query
    ''' # noqa:E501
    session_url = ctx.app_cfg.url
    subsequent = ctx.app_cfg.subsequent
    fmt = ctx.app_cfg.format

    with sql.create_engine(session_url).connect() as conn:
        try:
            result: list[pd.DataFrame] = []

            for id, command in enumerate(exec_msg.to_dict(orient='records')):
                # Selecting needed format values
                pattern = r'\{(.*?)\}'
                tokens = re.findall(pattern, command['command'], flags=re.MULTILINE)
                try:
                    kv_fmt = {
                        token : fmt[token]
                        for token in tokens
                    }
                except KeyError as exc:
                    raise Exception('One of the tokens was not provided in the context') from exc # noqa:E501
                except TypeError as exc:
                    raise Exception('Format tokens were not provided in the context') from exc # noqa:E501

                # Selecting placeholders and validating the shape
                plh = plh_msg[plh_msg.cmd_id == id].drop(columns=['cmd_id'])
                pattern = r':(.*?)'
                tokens = re.findall(pattern, command['command'], flags=re.MULTILINE)
                if not plh.empty:
                    if len(tokens) == 0:
                        raise ValueError('No placeholders found in the command. Use: `:placeholder` format to mark a token as a placeholder') # noqa:E501

                    plh['row'] = plh.groupby(['token']).cumcount()
                    plh = (
                        plh
                            .pivot(
                                index=['row'],
                                columns=['token'],
                                values=['value'],
                            )
                            .reset_index(drop=True)
                    )
                    if plh.isnull().values.any():
                        raise ValueError('Please make sure every placeholder needed is in the dataframe') # noqa:E501
                    plh = plh.to_dict(orient='records')
                    # NOTE: this is bad, but I have no idea
                    # how to get rid of multi-column index better
                    plh = [
                            {
                                key[1]: value
                                for key, value in item.items()
                            }
                        for item in plh
                    ]
                else:
                    plh = []
                ret = conn.execute(sql.text(command['command'].format(**kv_fmt)),
                                   parameters=plh)
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
