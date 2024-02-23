from typing import Literal, overload

from malevich.square import Context
from malevich_space.schema import SpaceSetup

from ..constants import SPACE_CONFIG_INJECTION_KEY


@overload
def extract_space_ops(context: Context, noexcept: Literal[False]) -> SpaceSetup:
    pass

@overload
def extract_space_ops(context: Context, noexcept: Literal[True]) -> SpaceSetup | None:
    pass


def extract_space_ops(context: Context, noexcept: bool = False) -> SpaceSetup:
    if raw_ops := context.app_cfg.get(SPACE_CONFIG_INJECTION_KEY, None):
        try:
            return SpaceSetup(**raw_ops)
        except Exception:
            if noexcept:
                return None
            raise
    else:
        if noexcept:
            return None

        raise ValueError(
            "SpaceOps not found in context.app_cfg under key "
            + SPACE_CONFIG_INJECTION_KEY
        )



