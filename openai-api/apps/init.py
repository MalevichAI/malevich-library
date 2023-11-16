from malevich.square import Context, init
from openai import OpenAI
from pydantic import BaseModel

from ..models.configuration.base import Configuration
from ..models.configuration.image import ImageConfiguration
from ..models.configuration.text import TextConfiguration


@init()
def init_models(ctx: Context):
    """Initializes the models."""
    if 'openai_api_key' in ctx.app_cfg:
        base_cls = {
            'text': TextConfiguration,
            'image': ImageConfiguration
        }

        cls: BaseModel = base_cls.get(ctx.app_cfg.get('mode', 'text'), TextConfiguration)
        try:
            cfg_object = {}
            # FIXME: pydantic<2
            for _key in cls.__fields__.keys():
                if _key == 'api_key':
                    cfg_object[_key] = ctx.app_cfg['openai_api_key']
                elif _key in ctx.app_cfg:
                    cfg_object[_key] = ctx.app_cfg[_key]
            client = OpenAI(
                api_key=cfg_object['api_key'],
                max_retries=cfg_object.get('max_retries', 3),
                organization=cfg_object.get('organization', None)
            )
            conf = cls(**cfg_object)
        except Exception as e:
            raise Exception(
                "Found `openai_api_key` in app config, "
                "but failed to initialize OpenAI client. Incorrect or empty key"
            ) from e
    else:
        raise Exception(
            "Missing `openai_api_key` in app config. "
            "Please provide your OpenAI API key."
        )

    ctx.app_cfg['client'] = client
    ctx.app_cfg['conf'] = conf
