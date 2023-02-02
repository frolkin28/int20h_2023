from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from aiohttp.web_fileresponse import FileResponse
from aiohttp.web_routedef import RouteTableDef
from hackaton.config import INDEX_PATH

routes = RouteTableDef()


@routes.get('/')
async def get_root(request: Request) -> FileResponse:  # noqa
    return FileResponse(INDEX_PATH)


@routes.get('/health')
async def health_check(request: Request) -> Response:
    return web.json_response({'status': 'ok'}, status=200)
