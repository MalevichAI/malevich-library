import pandas as pd
from malevich import SpaceInterpreter, SpaceSetup
from malevich.models.injections import SpaceInjectable
from malevich.models.task.interpreted.space import SpaceTaskStage
from malevich.square import Context, Sink, processor

from .models import Execute


@processor()
def execute(
    input: Sink,
    context: Context[Execute]
):
    """
    Execute other flows and get results.

    ## Input:
    DataFrames, which will override flow inputs.

    ## Output:
    DataFrames, which will be returned by launched flow.

    ## Configuration:

    - args_map: list.
        List of collection aliases. Must be in order of input dataframes.

    - reverse_id: str.
        Reverse ID of flow, you want to run.

    - deployment_id: str, default None.
        Deployment ID of flow, you want to run.

    - prepare: bool, default False.
        Create new deployment and use it.

    - attach_to_last: bool, default False.
        Use the last created active deployment.

    -----
    Args:
        input (Sink): DataFrames for the flow you want to launch.
    Returns:
        DataFrames, which will be returned by launched flow.
    """
    if context.common is None:
        context.common = {}
        context[context.operation_id] = 0
    elif context.operation_id not in context.common:
        context[context.operation_id] = 0

    if context.common[context.operation_id] > 5:
        print("Limit exceeded")
        result = []
        for i in input:
            result.append(i[0])
        return result

    args_map = context.app_cfg.get("args_map", None)
    assert args_map, "Argument mapping was not provided"
    reverse_id = context.app_cfg.get("reverse_id", None)
    assert reverse_id, "Reverse ID was not provided"

    empty = True
    for i in input:
        if len(i) > 1:
            context.logger.warn("There's more than one DF in DFS")
        if len(i[0]) != 0:
            empty = False
            break
    if empty:
        return pd.DataFrame([True], columns=['done'])

    deployment_id = context.app_cfg.get('deployment_id', None)
    prepare = context.app_cfg.get('prepare', False)
    attach = context.app_cfg.get('attach_to_last', False)
    assert (
         deployment_id or
         prepare or
         attach
        ), (
             "One of the following options should be provided: "
             "deployment_id, prepare, attach_to_last"
        )

    setup = SpaceSetup(**context.app_cfg.get('__space__'))
    setup.api_url = setup.api_url.replace('/api/v1', '')
    interpreter = SpaceInterpreter(setup)
    if deployment_id:
        task = interpreter.attach(reverse_id, deployment_id)
    elif prepare:
        task = interpreter.attach(reverse_id)
        task.prepare()
    elif attach:
        task = interpreter.attach(reverse_id, attach_to_last=True)
    else:
        raise ValueError("One of the following options should be provided: "
             "deployment_id, prepare, attach_to_last")

    assert task.get_stage() == SpaceTaskStage.STARTED

    injs: list[SpaceInjectable] = task.get_injectables()
    assert_injs = []
    for inj in injs:
        assert_injs.append(inj.alias)
    assert set(assert_injs) == set(args_map), "Flow collection aliases are not the same as provided"  # noqa: E501

    override = {}
    for i in range(len(args_map)):
        if len(input[i]) != 0:
            override[args_map[i]] = input[i][0]
    context.common[context.operation_id] += 1
    task.run(override=override)
    context.common[context.operation_id] = 0
    results = task.results()[0].get_dfs()
    if prepare:
        task.stop()
    if len(results) == 1:
        return results[0]
    else:
        return results
