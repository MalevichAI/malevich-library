import inspect
from typing import Callable

import dill
from malevich.square import OBJ, Context, Docs, processor


def _run(
    func: Callable,
    data: list[dict],
    data_param: inspect.Parameter,
    config: dict | None = None,
    config_param: inspect.Parameter | None = None
):
    locals_ = {
        'data': data,
        'config': config,
    }
    globals_ = {
        'func': func,
    }
    if data_param.kind == inspect.Parameter.POSITIONAL_ONLY:
        if config_param is not None:
            return eval(f'func(data, {config_param.name}=config)', globals_, locals_)
        return eval('func(data)', globals_, locals_)
    else:
        if config_param is not None:
            return eval(f'func({data_param.name}=data, {config_param.name}=config)', globals_, locals_)  # noqa: E501
        return eval(f'func({data_param.name}=data)', globals_, locals_)

@processor()
def run(func: OBJ, data: Docs, context: Context) -> Docs:
    fn, _ = dill.loads(open(func.path, 'rb').read())
    signature = inspect.signature(fn)
    config_param: str = context.app_cfg.get('run_config_param', None)
    data_param = context.app_cfg.get('run_data_param', None)
    batch_run = context.app_cfg.get('run_batch', False)
    map_to_dict = context.app_cfg.get('run_map_to_dict', True)

    if config_param is not None:
        for param in signature.parameters.values():
            if param.name == config_param:
                config_param = param
                break
        else:
            context.logger.warn(
                f"Function {fn.__name__} does not have a parameter named {config_param}. "
                "Ignoring the config parameter."
            )
            config_param = None

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

    annotation = data_param.annotation
    final_data = [d.dict() for d in data]
    if annotation != inspect.Parameter.empty:
        # If annotated as list
        if len(list(data)) == 1 and not batch_run:
            if annotation is list:
                final_data = [d.dict() for d in data]
            elif annotation is dict:
                final_data = data[0].dict()
            else:
                context.logger.warn(
                    f"Data parameter {data_param.name} is annotated as {annotation}. "
                    "It should be annotated as list[dict[str, Any]] or dict[str, Any]."
                )
        elif annotation is dict and not batch_run:
            context.logger.warn(
                f"The function {fn.__name__} expects a single dict, but the processor received multiple documents."  # noqa: E501
            )

    outputs = []
    if batch_run:
        for d in final_data:
            _run(fn, d, data_param)
            outputs.append(_run(fn, d, data_param, context.app_cfg, config_param))
    else:
        outputs.append(_run(fn, final_data, data_param, context.app_cfg, config_param))

    for i in range(len(outputs)):
        if not isinstance(outputs[i], dict):
            context.logger.warn(
                f"Function {fn.__name__} returned a non-dict type. "
                "The processor expects a dict as output."
            )
            if map_to_dict:
                try:
                    context.logger.warn("Trying to map the output to a dict.")
                    outputs[i] = outputs[i].__dict__
                except Exception:
                    raise ValueError(
                        f"Function {fn.__name__} returned a non-dict type and could "
                        "not be mapped to a dict."
                    )
            else:
                raise ValueError(
                    f"Function {fn.__name__} returned a non-dict type. "
                    "The processor expects a dict as output."
                )

    return outputs

