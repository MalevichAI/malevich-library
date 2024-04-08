import json
import pickle
import sys
from base64 import b64encode

import pydantic
from malevich import table
from malevich.core_api import AppFunctionsInfo
from malevich.install.iso import IsolatedSpaceInstaller
from malevich.square import DF, Context, processor, scheme
from malevich_space.schema import LoadedComponentSchema


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
    reverse_id: str

@processor()
def get_tree(packages: DF[Packages], code: DF[Code], ctx: Context[GetTreeConfig]):
    installer = IsolatedSpaceInstaller()
    for index, row in packages.iterrows():
        try:
            component = LoadedComponentSchema(**json.loads(row.loaded_component_json))
        except (json.JSONDecodeError, pydantic.ValidationError) as e:
            ctx.logger.error(f'Invalid LoadedComponentSchema JSON at {index}')
            raise e

        try:
            app_info = AppFunctionsInfo(**json.loads(row.app_info_json))
        except (json.JSONDecodeError, pydantic.ValidationError) as e:
            ctx.logger.error(f'Invalid AppFunctionsInfo JSON at {index}')
            raise e

        installer.install(row.package_name, component, app_info)

    trees = []
    for index, row in code.iterrows():
        for x in list(sys.modules.keys()):
            if x.startswith('malevich'):
                sys.modules.pop(x)

        from malevich import flow
        @flow(reverse_id=ctx.app_cfg.get('reverse_id'))
        def __flow() -> None:
            try:
                exec(row.code)
            except Exception as e:
                ctx.logger.error(f"Could not execute code at index {index}")
                raise e
        task = __flow()
        trees.append(
            b64encode(pickle.dumps(task.tree.model_dump(exclude=['results'])))
        )

    return table(trees, columns=['base64_tree'])
