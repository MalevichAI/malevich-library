import asyncio

from malevich.square import Context, Doc, Docs, processor

import aiohttp

from ..models import Connection, RequestScheme, ResponseScheme


@processor()
async def put(
    requests: Docs[RequestScheme],
    session_headers: Doc,
    context: Context[Connection]
) -> Doc[ResponseScheme]:
    cfg = context.app_cfg
    results = []
    async with aiohttp.ClientSession(
        cfg.base_url,
        headers=session_headers.parse(), 
        conn_timeout=cfg.timeout
    ) as session:
        rq = requests.parse(recursive=True)
        for r in rq:
            async with session.put(
                r.request.format(**r.path_kwargs) if r.path_kwargs else r.request,
                json=r.body,
                params=r.query,
                headers=r.headers
            ) as resp:
                result = await resp.json()
                if not resp.ok:
                    if cfg.raise_on_error:
                        raise Exception(
                            f'Status code: {resp.status}, response: {resp.reason}'
                        )
                    else:
                        context.logger.error(
                            f'Status code: {resp.status}, response: {resp.reason}'
                        )
                results.append(result)
            if cfg.interval:
                await asyncio.sleep(cfg.interval)

    return ResponseScheme(
        responses=results[0]
    ) if len(results) == 1 else ResponseScheme(responses=results)
