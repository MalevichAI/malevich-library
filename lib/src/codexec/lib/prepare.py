import inspect

import dill
from malevich.square import OBJ, Context


def parse_params(func: OBJ, context: Context):
    fn, _ = dill.loads(open(func.path, 'rb').read())
    signature = inspect.signature(fn)
    ctx_param: str = context.app_cfg.get('run_context_param', None)
    data_param = context.app_cfg.get('run_data_param', None)

    if ctx_param is not None:
        for param in signature.parameters.values():
            if param.name == ctx_param:
                ctx_param = param
                break
        else:
            context.logger.warn(
                f"Function {fn.__name__} does not have a parameter named {ctx_param}. "
                "Ignoring the config parameter."
            )
            ctx_param = None

    if data_param is not None:
        for param in signature.parameters.values():
            if param.name == data_param:
                data_param = param
                break
        else:
            raise ValueError(
                f"Function {fn.__name__} does not have a parameter named {data_param}."
            )


    no_defaults = []
    for param in signature.parameters.values():
        if param.default == inspect.Parameter.empty:
            no_defaults.append(param)

    if len(no_defaults) == 0 and data_param is None:
        context.logger.warn(
            f"Function {fn.__name__} has no parameters without default values. "
            "Will try to set first positional-only parameter as data."
        )
        pos_only = [
            param for param in signature.parameters.values()
            if param.kind == inspect.Parameter.POSITIONAL_ONLY
        ]
        if len(pos_only) == 1:
            data_param = pos_only[0]

        if data_param is None:
            data_param = next(iter(signature.parameters.values()))
            context.logger.warn(
                f"Function {fn.__name__} has no positional-only parameters. "
                f"Setting first parameter {data_param.name} as data."
            )
    elif len(no_defaults) == 1 and data_param is None:
        data_param = no_defaults[0]
    elif len(no_defaults) > 1 and data_param is None:
        raise ValueError(
            f"Function {fn.__name__} has multiple parameters without default values. "
            "The processor can only run functions with one parameter without default values. "  # noqa: E501
        )

    return fn, data_param, ctx_param

