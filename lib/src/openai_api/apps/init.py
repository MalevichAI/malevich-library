from malevich.square import Context, init

from ..models.configuration.base import Configuration


@init()
def init_models(ctx: Context):
    """Initializes the models."""
    if 'openai_api_key' in ctx.app_cfg:
        cfg_object = {}

        conf = None
        for _key in Configuration.__fields__.keys():
            if _key == 'api_key':
                cfg_object[_key] = ctx.app_cfg['openai_api_key']
            elif _key in ctx.app_cfg:
                cfg_object[_key] = ctx.app_cfg[_key]

        conf = Configuration(**cfg_object)

        if conf is None:
            raise Exception(
                "Found `openai_api_key` in app config, "
                "but failed to initialize OpenAI client. "
                "Incorrect or empty key or wrong mode"
            )
    else:
        raise Exception(
            "Missing `openai_api_key` in app config. "
            "Please provide your OpenAI API key."
        )

    ctx.app_cfg['conf'] = conf
