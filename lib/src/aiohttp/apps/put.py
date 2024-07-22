import aiohttp
from malevich.square import Doc, Context, processor, scheme
from pydantic import BaseModel
import asyncio
from ..models import Connection


@scheme()
class PutScheme(BaseModel):
    request: str
    path_kwargs: dict | None
    body: dict | None
    query: dict | None
    headers: dict | None
    
@scheme()
class PutResponses(BaseModel):
    responses: list[dict]

@processor()
async def put(
    requests: Doc[PutScheme],
    session_headers: Doc,
    context: Context[Connection]
) -> Doc[PutResponses]:
    cfg = context.app_cfg
    results = []
    async with aiohttp.ClientSession(
        cfg.base_url,
        headers=session_headers.parse(), 
        conn_timeout=cfg.timeout
    ) as session:
        rq = requests.parse()
        async with session.put(
            rq.request.format(**rq.path_kwargs) if rq.path_kwargs else rq.request, 
            json=rq.body, 
            params=rq.query, 
            headers=rq.headers
        ) as resp:
            result = await resp.json()
            if resp.status != 200:
                raise Exception(f'Status code: {resp.status}, response: {resp.reason}')
            results.append(result)
        if cfg.interval:
            await asyncio.sleep(cfg.interval)
    return PutResponses(responses=results)