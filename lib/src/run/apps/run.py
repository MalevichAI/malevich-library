import inspect
from typing import Any

import pandas as pd
from malevich.square import OBJ, Context, Docs, processor

from lib.prepare import parse_params
from lib.safe_run import local_safe_run


def validate_batched_output(output: Any):
    return isinstance(output, dict) or isinstance(output, pd.DataFrame)

def validate_single_output(output: Any):
    return (
        # Doc
        isinstance(output, dict)
        # DF
        or isinstance(output, pd.DataFrame)
        # DFS
        or (isinstance(output, list) and all(isinstance(o, pd.DataFrame) for o in output))
        # Docs
        or (isinstance(output, list) and all(isinstance(o, dict) for o in output))
    )

def validate_output(output: Any, batched: bool):
    if not batched:
        if isinstance(output, tuple):
            for i, o in enumerate(output):
                if not validate_single_output(o):
                    raise ValueError(
                        f"The output at index {i} can be: dict (Doc), pd.DataFrame (DF), "
                        "list of pd.DataFrame (DFS), or list of dict (Docs)."
                        f" But got {type(o)}."
                    )
        else:
            if not validate_single_output(output):
                raise ValueError(
                    "The output can be: dict (Doc), pd.DataFrame (DF), "
                    "list of pd.DataFrame (DFS), or list of dict (Docs)."
                    f" But got {type(output)}."
                )

    else:
        for i, o in enumerate(output):
            if not validate_batched_output(o):
                raise ValueError(
                    "When running in batch mode, "
                    f" the output at index {i} was {type(o)}, but expected dict or pd.DataFrame."  # noqa: E501
                )

@processor()
def run(func: OBJ, data: Docs, context: Context) -> Docs:
    """Executes a local function on the provided data

    A special processor that allows you to run a local function on an aribtrary data.
    The data can be a single document or a list of documents, but will always be
    passed to the function as a list of documents.

    A function can be executed in two modes:

    1. Batch mode: The function is executed for each document in the data. The output
    of the function is expected to be a dict or a DataFrame.
    2. Single mode: The function is executed once for the entire data. The output
    of the function is expected to be a dict, a DataFrame, a list of dicts, or a list of DataFrames.

    Additionally, the function can take an optional context parameter that can be used
    to pass run-bound parameters to the function.

    ## Input:
        - `func`: A function captured with Malevich `asset.capture_function`.
        - `data`: An arbitrary data to be passed to the function.

    ## Output:
        - The output of the function.

    ## Configuration:
        - `run_batch`: bool, default False.
            If True, the function will be executed in batch mode.
        - `run_context_param`: str, default None.
            The name of the context parameter in the function.
        - `run_data_param`: str, default None.
            The name of the data parameter in the function.
            If None, the first parameter without a default value will be used.
        - `dependencies`: list, default None
            List of modules to import.

    -----
    Args:
        func (OBJ): The function to be executed.
        data (Docs): The data to be passed to the function.
        context (Context): The context object.
    """
    batch_run = context.app_cfg.get('run_batch', False)

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
            outputs.append(local_safe_run(fn, d, data_param, context, config_param))
    else:
        outputs = local_safe_run(fn, final_data, data_param, context, config_param)

    validate_output(outputs, batch_run)
    return outputs

