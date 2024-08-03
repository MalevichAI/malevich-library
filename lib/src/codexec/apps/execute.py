from typing import Any, Callable

import dill
from malevich.square import Docs, OBJ, Context, processor


def preprocess(source_code, raw_data: list[dict]):
    # TODO: Implement preprocessing logic with LLM
    return tuple(), dict()

def postprocess(source_code, output: Any):
    # TODO: Implement postprocessing logic with LLM
    return output or {}

def safe_exec(function: Callable, *args, **kwargs):
    return eval('function(*args, **kwargs)', {}, {
        'args': args,
        'kwargs': kwargs,
        'function': function
    })


@processor()
def execute_code(func: OBJ, data: Docs, context: Context):
    fn, source_code = dill.loads(open(func.path, 'rb').read())
    args, kwargs = preprocess(source_code, [d.dict() for d in data])
    output = safe_exec(fn, *args, **kwargs)
    return postprocess(source_code, output)
