from aiohttp import web
from aiohttp.web_fileresponse import FileResponse
from hackaton.config import INDEX_PATH


async def index(_: web.Request) -> web.Response:
    return FileResponse(INDEX_PATH)
