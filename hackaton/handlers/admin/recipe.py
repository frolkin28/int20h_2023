from aiohttp import web

from hackaton.tasks.recipe import (
    calculate_difficulty_level_for_all_recipes
    as _calculate_difficulty_level_for_all_recipes
)

async def calculate_difficulty_level_for_all_recipes(request):
    result = await _calculate_difficulty_level_for_all_recipes()
    return web.json_response({'result': result}, status=200)