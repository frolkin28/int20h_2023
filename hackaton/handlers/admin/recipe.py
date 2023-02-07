from aiohttp import web

from hackaton.tasks.recipe import (
    calculate_difficulty_level_for_all_recipes
    as _calculate_difficulty_level_for_all_recipes,
    add_ingredients_ids_field_for_all_recipes
    as _add_ingredients_ids_field_for_all_recipes,
)

async def calculate_difficulty_level_for_all_recipes(request):
    result = await _calculate_difficulty_level_for_all_recipes()
    return web.json_response({'result': result}, status=200)


async def calculate_difficulty_level_for_all_recipes(request):
    result = await _calculate_difficulty_level_for_all_recipes()
    return web.json_response({'result': result}, status=200)


async def add_ingredients_ids_field_for_all_recipes(request):
    result = await _add_ingredients_ids_field_for_all_recipes()
    return web.json_response({'result': result}, status=200)