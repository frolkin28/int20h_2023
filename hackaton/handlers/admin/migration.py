from aiohttp import web

from hackaton.tasks.mealdb.recipe_category import (
    migrate_recipe_categories as _migrate_recipe_categories
)


async def migrate_recipe_categories(request: web.Request) -> web.Response:
    await _migrate_recipe_categories(app=request.app)

    return web.json_response({'status': 'ok'}, status=200)
