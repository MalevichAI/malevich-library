import asyncio

async def coroutine(
    timeout: int
):
    await asyncio.sleep(timeout)