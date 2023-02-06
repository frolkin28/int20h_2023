from http import client as httplib
from logging import getLogger

from aiohttp import web

from hackaton.lib.query import get_recipe_by_id
from hackaton.lib.rest_utils import error_response
from hackaton.lib.rest_utils import ok_response
from hackaton.lib.payloads.schemas import RecipeSchema


async def recipe_view(request: web.Request) -> web.Response:
    recipe_id = request.match_info['id']
    recipe = await get_recipe_by_id(recipe_id)
    if not recipe:
        return error_response(code=httplib.NOT_FOUND)

    recipe_data = RecipeSchema().dump(recipe)
    return ok_response(payload=recipe_data)
