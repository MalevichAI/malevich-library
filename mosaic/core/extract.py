from typing import Literal, overload

from malevich.square import Context

from ..constants import CORE_CONFIG_INJECTION_KEY


@overload
def extract_core_ops(context: Context, noexcept: Literal[False]) -> dict:
    # TODO: Add schema: https://github.com/MalevichAI/malevich/issues/31 
    pass

@overload
def extract_core_ops(context: Context, noexcept: Literal[True]) -> dict:
    # TODO: Add schema: https://github.com/MalevichAI/malevich/issues/31 
    pass


def extract_core_ops(context: Context, noexcept: bool = False) -> dict | None:
    if raw_core := context.app_cfg.get(CORE_CONFIG_INJECTION_KEY, None):
       if isinstance(raw_core, dict):
           return raw_core
       else:
           if noexcept:
               return None
           raise ValueError(
               "Expected a dictionary for {CORE_CONFIG_INJECTION_KEY} "
               f"but got {type(raw_core)}"
           )
