import argparse 
from jls_utils import *

parser = argparse.ArgumentParser()
parser.add_argument("-H", default="http://localhost:8080")
parser.add_argument("-i", default="utility", help="Docker image name")
parser.add_argument("--random-image", 
                    default="registry.gitlab.com/h1054/julius-internal-app-directory/malevich-app-library/boot/random:random", 
                    help="Docker image for Boot.Random application")


if __name__ == '__main__':
    args = parser.parse_args()
    # Set a mock user and pass
    update_core_credentials("user", "pass")

    # Set the host and port
    set_host_port(args.H)

    # Create a user
    try: delete_user()
    except: pass
    finally: create_user()

    # Create an application 
    # that generates a random dataframe
    create_app(
        app_id="random",
        processor_id="generate_random_df_from_cols",
        # empty input
        # but there is no way
        # to run the first app
        # without input
        app_cfg={
            "nrows": 10,
            "columns": {
                "A": {
                    "type": "number"
                },
                "B": {
                    "type": "name"
                },
                "C": {
                    'type': 'datetime',
                    'from_date': '2020-01-01',
                    'to_date': '2020-12-31'
                }
            }
        },
        image_ref=args.random_image
    )

    # The major app: 
    # Selects a subset of the dataframe
    create_app(
        app_id="rename_column",
        processor_id="rename_column",
        app_cfg={
            "A": "renamed",
        },
        image_ref="utility_rename"
    )

    # jls_random -> jls_select
    create_task(task_id="task", app_id="rename_column", apps_depends=["random"])

    # Run the task
    create_cfg("jls_random_output", {})


    task_full(task_id="task", cfg_id="jls_random_output", profile_mode='all')
