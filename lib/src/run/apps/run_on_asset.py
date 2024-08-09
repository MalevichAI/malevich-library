from malevich.square import OBJ, Context, processor

from lib.prepare import parse_params
from lib.safe_run import local_safe_run


@processor()
def run_on_asset(func: OBJ, asset: OBJ, context: Context):
    """Executes a local function on the provided asset

    A special processor that allows you to run a local function on an aribtrary asset.
    The asset can be any kind of file, but will always be passed to the function as a path.

    The function is supposed to accept str-like path as the first argument. Additionally,
    the function can accept a run-bound context as the keyword argument.

    ## Input:
        - `func`: The function to be executed.
        - `asset`: The asset to be passed to the function.

    ## Output:
        The output of the function.

    ## Configuration:
        - `run_data_param`: str, default None.
            The name of the parameter that will be passed the data.
            If None, the first positional parameter will be used.
        - `run_context_param`: str, default None.
            The name of the parameter that will be passed the context.
            If None, the function will be called without the context parameter.
    -----
    """  # noqa: E501
    fn, data_param, config_param = parse_params(func, context)
    return local_safe_run(fn, asset.path, data_param, context, config_param)

