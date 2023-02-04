import asyncio

from aiohttp import web

from hackaton.tasks.mealdb.ingredient import migrate_ingredients
from hackaton.tasks.mealdb.recipe import migrate_recipes_by_categories
from hackaton.tasks.mealdb.recipe_category import migrate_recipe_categories


async def mealdb_full_migration(app: web.Application) -> None:
    parallel_tasks = [
        migrate_ingredients(app),
        migrate_recipe_categories(app),
    ]
    await asyncio.gather(*parallel_tasks)
    await migrate_recipes_by_categories(app)