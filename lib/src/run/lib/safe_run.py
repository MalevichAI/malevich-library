import inspect
from typing import Any, Callable

from malevich.square import Context


def local_safe_run(
    func: Callable,
    data: Any,
    data_param: inspect.Parameter,
    config: Context | None = None,
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
