from malevich.square import Context, init

from .linear import LinearExecutor


@init()
def init_linear_executor(context: Context):
    if not context.app_cfg.get('linear_api_key'):
        raise RuntimeError('Please, provide a Linear API Key')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': context.app_cfg['linear_api_key']
    }
    context.common = LinearExecutor('https://api.linear.app/graphql', headers)
