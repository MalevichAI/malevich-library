import json
import pickle
import sys
from base64 import b64encode

from malevich import table
from malevich.core_api import AppFunctionsInfo
from malevich.install.iso import IsolatedSpaceInstaller
from malevich.square import DF, Context, processor, scheme
from malevich_space.schema import LoadedComponentSchema
from pydantic import Field, ValidationError


@scheme()
class Packages:
    package_name: str
    loaded_component_json: str
    app_info_json: str


@scheme()
class Code:
    code: str

@scheme()
class GetTreeConfig:
    reverse_id: str = Field(
        ...,
        description="A reverse ID that should be used when interpreting"
                    " the code. Used if only body is provided"
    )

    only_body: bool = Field(
        True, description="Set to True, if only body of @flow function is provided"
    )

    flow_name: str | None = Field(
        None,
        description="A name of the flow to be interpreted "
                    "if multiple @flow function is detected."
    )


@processor()
def get_tree(packages: DF[Packages], code: DF[Code], ctx: Context[GetTreeConfig]):
    """Retrieves an execution tree from Malevich metascript

    ## Input:
        A dataframe that contains a list of packages to be installed, and
        a dataframe with code chunks.

        The first one contains the following columns:
            - `package_name` (str): A name of the package to install.
            - `loaded_component_json` (str):
                JSON serialized LoadedComponentSchema object.
            - `app_info_json` (str): JSON serialized AppFunctionsInfo object.

        ---

        The second one contains a single column:
            - `code` (str): code chunk (either full metascript or @flow function body)

    ## Output:

        A dataframe with a single column:
            - `base64_tree` (str): Base64 encoded TreeNode object.

    ## Configuration:
        - reverse_id: str.
            A reverse ID that should be used when interpreting the code.
            Used if only body is provided.
        - only_body: bool, default True.
            Set to True, if only body of @flow function is provided.
        - flow_name: str, default None.
            A name of the flow to be interpreted if multiple @flow function is detected.

    -----

    Args:
        packages (table): A table of packages to be installed.
        code (table): A table of code snippets to be executed.

    Returns:
        A dataframe with a column `base64_tree` that contains
        base64 encoded TreeNode objects.
    """
    installer = IsolatedSpaceInstaller()
    for index, row in packages.iterrows():
        try:
            component = LoadedComponentSchema(**json.loads(row.loaded_component_json))
        except (json.JSONDecodeError, ValidationError) as e:
            ctx.logger.error(f'Invalid LoadedComponentSchema JSON at {index}')
            raise e

        try:
            app_info = AppFunctionsInfo(**json.loads(row.app_info_json))
        except (json.JSONDecodeError, ValidationError) as e:
            ctx.logger.error(f'Invalid AppFunctionsInfo JSON at {index}')
            raise e

        installer.install(row.package_name, component, app_info)

    trees = []
    for index, row in code.iterrows():
        for x in list(sys.modules.keys()):
            if x.startswith('malevich'):
                sys.modules.pop(x)
        if ctx.app_cfg.only_body:
            from malevich import flow
            @flow(reverse_id=ctx.app_cfg.get('reverse_id'))
            def __flow() -> None:
                try:
                    exec(row.code)
                except Exception as e:
                    ctx.logger.error(f"Could not execute code at index {index}")
                    raise e
        else:
            from malevich._meta.flow import FlowFunction
            try:
                exec(row.code)
            except Exception as e:
                ctx.logger.error(f"Could not execute code at index {index}")
                raise e
            __flow = None
            for name_, object_ in locals().items():
                if isinstance(object_, FlowFunction):
                    if __flow is not None:
                        if ctx.app_cfg.flow_name is None:
                            raise Exception(
                                "Multiple @flow function found in metascript"
                                " and flow_name is not provided in configuration."
                            )
                        elif name_ == ctx.app_cfg.flow_name:
                            __flow = object_
                    else:
                        __flow = object_
        if __flow is None or not isinstance(__flow, FlowFunction):
            message = "Failed to find a flow. "
            if ctx.app_cfg.flow_name is not None:
                message += "None of @flow functions is named as "
                message += ctx.app_cfg.flow_name
            raise Exception(message)
        task = __flow()

        trees.append(
            b64encode(pickle.dumps(task.tree.model_dump(exclude=['results'])))
        )

    return table(trees, columns=['base64_tree'])
