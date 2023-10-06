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
        app_id="random_1",
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
    
    create_app(
        app_id="random_2",
        processor_id="generate_random_df_from_cols",
        # empty input
        # but there is no way
        # to run the first app
        # without input
        app_cfg={
            "nrows": 10,
            "columns": {
                "X": {
                    "type": "number"
                },
                "Y": {
                    "type": "number"
                },
            }
        },
        image_ref=args.random_image
    )
    

    # The major app: 
    # Selects a subset of the dataframe
    create_app(
        app_id="sink",
        processor_id="sink_2",
        image_ref="utility_sink"
    )
    
    create_app(
        app_id="check",
        processor_id="__test",
        image_ref="utility_sink"
    )


    create_task(task_id="task", app_id="sink", apps_depends=["random_1", "random_2"])
    create_task(task_id="check", app_id="check", tasks_depends=["task"])
    

    # Run the task
    create_cfg("сfg", {})


    task_full(task_id="check", cfg_id="сfg", profile_mode='all')
