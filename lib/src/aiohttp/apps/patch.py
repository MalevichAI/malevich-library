import aiohttp
from malevich.square import Doc, Docs, Context, processor, scheme
from pydantic import BaseModel
import asyncio
from ..models import Connection, RequestScheme, ResponseScheme, Requests


@processor()
async def patch(
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
        rq = requests.parse(recurse=True)
        for r in rq:
            async with session.patch(
                r.request.format(**r.path_kwargs) if r.path_kwargs else r.request, 
                json=r.body, 
                params=r.query, 
                headers=r.headers
            ) as resp:
                result = await resp.json()
                if resp.status != 200:
                    raise Exception(f'Status code: {resp.status}, response: {resp.reason}')
                results.append(result)
            if cfg.interval:
                await asyncio.sleep(cfg.interval)
    return ResponseScheme(responses=results) if len(results) > 1 else ResponseScheme(responses=results[0])
