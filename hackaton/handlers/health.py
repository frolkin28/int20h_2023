from aiohttp import web


async def health_check(request: web.Request) -> web.Response:
    return web.json_response({'status': 'ok'}, status=200)
