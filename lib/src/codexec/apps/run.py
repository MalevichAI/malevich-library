import inspect

import dill
from malevich.square import OBJ, Context, Docs, processor

from lib.prepare import parse_params
from lib.safe_run import local_safe_run


@processor()
def run(func: OBJ, data: Docs, context: Context) -> Docs:
    batch_run = context.app_cfg.get('run_batch', False)
    map_to_dict = context.app_cfg.get('run_map_to_dict', True)

    fn, data_param, config_param = parse_params(func, context)

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
            local_safe_run(fn, d, data_param)
            outputs.append(local_safe_run(fn, d, data_param, context, config_param))

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
    else:
        outputs = local_safe_run(fn, final_data, data_param, context, config_param)

    print(type(outputs), len(outputs))
    return outputs

