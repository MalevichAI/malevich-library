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
class FormatTokenMessage(BaseModel):
    token: str
    value: str

@scheme()
class PlaceholderMessage(BaseModel):
    cmd_id: int
    token: str
    value: Any

@processor()
def execute(
    exec_msg: DF[ExecuteMessage],
    fmt_msg: DF[FormatTokenMessage],
    plh_msg: DF[PlaceholderMessage],
    ctx: Context[Query]
) -> DFS:
    '''
    Execute raw SQL command on the database.


    ## Input:

        - `exec_msg` (DF[ExecuteMessage]): actual commands
        - `fmt_msg` (DF[FormatTokenMessage]): format values for tokens in the commands

    ## Output:

        A list of dataframs with a result for each query. If the query does not return any values, a dataframe with a single column `rows_affected` is returned.

    ## Configuration:

        - `url` (str): URL of the DB to connect to
        - `subsequent` (bool): if True, each statement will be commited before the next one is executed

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
                plh = plh_msg[plh_msg.cmd_id == id].drop(columns=['cmd_id'])
                if not plh.empty:
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
                # TODO: introduce placeholders
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
