from aiohttp import web

from hackaton.tasks.mealdb import (
    mealdb_full_migration as _mealdb_full_migration
)
from hackaton.tasks.mealdb.recipe import (
    migrate_recipes_by_categories as _migrate_recipes_by_categories
)
from hackaton.tasks.mealdb.recipe_category import (
    migrate_recipe_categories as _migrate_recipe_categories
)
from hackaton.tasks.mealdb.ingredient import (
    migrate_ingredients as _migrate_ingredients
)


async def migrate_recipe_categories(request: web.Request) -> web.Response:
    await _migrate_recipe_categories(app=request.app)

    return web.json_response({'status': 'ok'}, status=200)


async def migrate_ingredients(request: web.Request) -> web.Response:
    await _migrate_ingredients(app=request.app)

    return web.json_response({'status': 'ok'}, status=200)


async def migrate_recipes_by_categories(request: web.Request) -> web.Response:
    await _migrate_recipes_by_categories(app=request.app)

    return web.json_response({'status': 'ok'}, status=200)


async def mealdb_full_migration(request: web.Request) -> web.Response:
    await _mealdb_full_migration(app=request.app)

    return web.json_response({'status': 'ok'}, status=200)
