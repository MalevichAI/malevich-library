import argparse
import random
import string
import os

import pandas as pd
import jls_utils as ju

from typing import Tuple, Union
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument('-i', default='utility')
parser.add_argument('-H', default='http://localhost:8080')


def random_str(str_len: int) -> str:
    return "".join([random.choice(string.ascii_lowercase) for _ in range(str_len)])


def random_df() -> Tuple[Union[Path, str], pd.DataFrame]:
    script_dir = os.path.dirname(os.path.realpath(__file__))
    data_frame_path = os.path.join(Path(script_dir).parent, 'data', 'exp_df.csv')

    df_cols = {"col1": [random_str(10) for _ in range(5)],  # str data
               "col2": [random.randint(a=1, b=10) for _ in range(5)],  # int data
               "col3": [random_str(10) for _ in range(5)],  # str data
               "col4": [random.random() for _ in range(5)]}  # float data

    df = pd.DataFrame(data=df_cols, index=list(range(5)))

    # save the dataframe to the path
    df.to_csv(data_frame_path, index=False)

    return data_frame_path, df


def main():
    args = parser.parse_args()

    ju.update_core_credentials(username=random_str(str_len=20), password='pass_0')

    try:
        ju.delete_user()
    except:
        pass
    finally:
        ju.set_host_port(args.H)
        ju.create_user()

    script_dir = os.path.dirname(os.path.realpath(__file__))
    df_path, df = random_df()
    # print(df)

    # create the collection from the dataframe
    pattern_match_collection = ju.create_collection_from_file(df_path)
    # let's set the configuration
    basic_config = {'pattern': r'[aeuioy]{2}', "join_str": "*-*"}

    ju.create_app(
        # the app_id is present in the processor file of the utility/match_pattern directory
        app_id='match_pattern_app',
        processor_id='pattern_match_processor',
        input_id='match_pattern_input',
        image_ref=args.i,
        app_cfg=basic_config
    )

    ju.create_task(task_id='match_pattern_task',
                   app_id='match_pattern_app')

    # create the collection
    task_configuration = {
        "collections": {
            'match_pattern_collection': pattern_match_collection
        }
    }

    ju.create_cfg('main_cfg', task_configuration)
    ju.task_full('match_pattern_task', 'main_cfg', with_show=True, profile_mode='df_show')


if __name__ == '__main__':
    main()
