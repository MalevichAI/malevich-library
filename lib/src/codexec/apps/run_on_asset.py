from malevich.square import OBJ, Context, processor

from lib.prepare import parse_params
from lib.safe_run import local_safe_run


@processor()
def run_on_asset(func: OBJ, asset: OBJ, context: Context):
    fn, data_param, config_param = parse_params(func, context)
    return local_safe_run(fn, asset.path, data_param, context, config_param)

